import numpy as np
import pandas as pd
import streamlit as st

from agent import get_recommendation
from dashboard.charts import attendance_chart, engagement_chart
from dashboard.reports import generate_report
from engagement import classify_engagement
from fusion import FusionEngine
from storage import (
	create_database,
	get_present_student_count,
	get_recent_engagement,
	save_attendance,
	save_engagement,
)


def audio_engagement_level(speech_ratio):
	if speech_ratio >= 60:
		return "High"
	if speech_ratio >= 30:
		return "Moderate"
	return "Low"


st.set_page_config(
	page_title="Classroom Signal Board",
	page_icon="C",
	layout="wide",
	initial_sidebar_state="expanded",
)

st.markdown(
	"""
	<style>
	:root {
		--ink: #1d302d;
		--muted: #64746f;
		--green: #087f73;
	}
	.stApp {
		background: linear-gradient(135deg, #f3f6f2 0%, #edf4f2 55%, #f7f3eb 100%);
		color: var(--ink);
	}
	[data-testid="stSidebar"] {
		background: #e8efeb;
		border-right: 1px solid #d6e0da;
	}
	.block-container {
		max-width: 1440px;
		padding-top: 2rem;
		padding-bottom: 3rem;
	}
	h1, h2, h3 {
		color: var(--ink);
		font-family: Georgia, "Times New Roman", serif;
		letter-spacing: 0;
	}
	[data-testid="stMetric"] {
		background: rgba(255, 255, 255, 0.78);
		border: 1px solid #dce5df;
		border-top: 3px solid var(--green);
		border-radius: 6px;
		padding: 14px 16px;
	}
	[data-testid="stMetricLabel"] { color: var(--muted); }
	[data-testid="stButton"] > button,
	[data-testid="stDownloadButton"] > button {
		border-radius: 5px;
		min-height: 2.6rem;
	}
	.eyebrow {
		color: var(--green);
		font-size: 0.76rem;
		font-weight: 700;
		text-transform: uppercase;
	}
	.subtle { color: var(--muted); }
	</style>
	""",
	unsafe_allow_html=True,
)


create_database()

if "attendance_roster" not in st.session_state:
	st.session_state.attendance_roster = pd.DataFrame(
		{
			"Student ID": [f"Student {index:03d}" for index in range(1, 26)],
			"Present": [False] * 25,
		}
	)
if "audio_result" not in st.session_state:
	st.session_state.audio_result = None
if "face_result" not in st.session_state:
	st.session_state.face_result = None


st.sidebar.markdown('<p class="eyebrow">Session controls</p>', unsafe_allow_html=True)
st.sidebar.header("Live signals")
attention = st.sidebar.slider("Attention", 0, 100, 78)
movement = st.sidebar.slider("Movement", 0, 100, 64)
activity = st.sidebar.slider("Class activity", 0, 100, 72)

audio_mode = st.sidebar.radio("Audio source", ["Manual score", "Microphone"])
if audio_mode == "Manual score":
	audio_score = st.sidebar.slider("Audio participation", 0, 100, 68)
	audio_result = None
else:
	if st.sidebar.button("Record 5-second sample", use_container_width=True):
		try:
			with st.spinner("Recording classroom audio..."):
				from audio import AudioModule

				st.session_state.audio_result = AudioModule(duration=5).analyze_audio()
		except Exception as error:
			st.sidebar.error(f"Audio capture failed: {error}")

	audio_result = st.session_state.audio_result
	if audio_result:
		audio_score = min(100, max(0, audio_result["speech_ratio"]))
		st.sidebar.metric("Speech ratio", f"{audio_result['speech_ratio']}%")
		st.sidebar.caption(
			f"Noise {audio_result['noise_level']}% · "
			f"{audio_engagement_level(audio_score)} participation"
		)
	else:
		audio_score = 68
		st.sidebar.caption("No sample recorded in this session.")


score = FusionEngine().calculate_engagement(
	attention,
	movement,
	activity,
	audio_score,
)
level = classify_engagement(score)
recommendation = get_recommendation(level, audio_score)
recent_sessions = get_recent_engagement()
roster = st.session_state.attendance_roster
roster_count = len(roster)
present_count = int(roster["Present"].fillna(False).astype(bool).sum()) if roster_count else 0

st.markdown('<p class="eyebrow">Classroom intelligence / live session</p>', unsafe_allow_html=True)
st.title("Classroom signal board")
st.markdown(
	'<p class="subtle">A measured view of participation, attendance, and session momentum.</p>',
	unsafe_allow_html=True,
)

overview_tab, attendance_tab, history_tab, report_tab = st.tabs(
	["Overview", "Attendance", "Session history", "Report"]
)

with overview_tab:
	metric_columns = st.columns(4)
	metric_columns[0].metric("Engagement score", f"{score:.1f} / 100")
	metric_columns[1].metric("Engagement level", level)
	metric_columns[2].metric("Roster present", f"{present_count} / {roster_count}")
	metric_columns[3].metric("Audio participation", f"{audio_score:.0f}%")

	chart_column, action_column = st.columns([1.25, 0.85], gap="large")
	with chart_column:
		st.subheader("Attendance snapshot")
		if st.session_state.face_result and roster_count:
			detected = min(st.session_state.face_result["count"], roster_count)
			st.plotly_chart(
				attendance_chart(detected, roster_count - detected),
				use_container_width=True,
				key="attendance_overview",
			)
		else:
			st.caption("Capture a visual check in Attendance to see detections.")

	with action_column:
		st.subheader("Session readout")
		st.markdown(f"**{level} engagement** · score {score:.1f}")
		st.write(recommendation)
		st.divider()
		if st.button("Save engagement session", type="primary", use_container_width=True):
			save_engagement(score, level, recommendation)
			st.success("Session saved to history.")

	st.subheader("Recent engagement")
	if recent_sessions:
		st.plotly_chart(
			engagement_chart(recent_sessions),
			use_container_width=True,
			key="engagement_overview",
		)
	else:
		st.caption("No saved engagement sessions yet.")

with attendance_tab:
	roster_column, camera_column = st.columns([1.2, 0.8], gap="large")

	with roster_column:
		st.subheader("Class roster")
		with st.form("attendance_form"):
			edited_roster = st.data_editor(
				st.session_state.attendance_roster,
				column_config={
					"Student ID": st.column_config.TextColumn("Student ID", required=True),
					"Present": st.column_config.CheckboxColumn("Present"),
				},
				hide_index=True,
				num_rows="dynamic",
				use_container_width=True,
				key="attendance_editor",
			)
			save_clicked = st.form_submit_button(
				"Save attendance snapshot",
				type="primary",
				use_container_width=True,
			)

		if save_clicked:
			records = []
			seen_ids = set()
			for _, row in edited_roster.iterrows():
				student_id = str(row["Student ID"]).strip()
				if student_id and student_id not in seen_ids:
					records.append((student_id, bool(row["Present"])))
					seen_ids.add(student_id)

			if records:
				for student_id, is_present in records:
					save_attendance(student_id, is_present)
				st.session_state.attendance_roster = pd.DataFrame(
					records,
					columns=["Student ID", "Present"],
				)
				st.success(
					f"Saved {sum(value for _, value in records)} present "
					f"of {len(records)} students."
				)
			else:
				st.warning("Add at least one student before saving attendance.")

		st.caption(
			f"{get_present_student_count()} distinct student IDs have been recorded present."
		)

	with camera_column:
		st.subheader("Visual check")
		camera_snapshot = st.camera_input("Capture a classroom snapshot")
		if camera_snapshot and st.button("Analyze faces in snapshot"):
			try:
				import cv2
				from vision import VisionModule

				image = cv2.imdecode(
					np.frombuffer(camera_snapshot.getvalue(), dtype=np.uint8),
					cv2.IMREAD_COLOR,
				)
				detector = VisionModule()
				try:
					annotated, face_count, _ = detector.detect_faces(image)
				finally:
					detector.face_detector.close()

				st.session_state.face_result = {
					"count": face_count,
					"image": cv2.cvtColor(annotated, cv2.COLOR_BGR2RGB),
				}
			except Exception as error:
				st.error(f"Snapshot analysis failed: {error}")

		if st.session_state.face_result:
			st.metric("Faces detected", st.session_state.face_result["count"])
			st.image(st.session_state.face_result["image"], use_container_width=True)
			st.caption("Face detection is not identity recognition; confirm attendance in the roster.")

with history_tab:
	st.subheader("Saved engagement sessions")
	if recent_sessions:
		history_frame = pd.DataFrame(recent_sessions).rename(
			columns={
				"timestamp": "Timestamp",
				"score": "Score",
				"level": "Level",
				"recommendation": "Recommendation",
			}
		)
		st.dataframe(history_frame, hide_index=True, use_container_width=True)
		st.plotly_chart(
			engagement_chart(recent_sessions),
			use_container_width=True,
			key="engagement_history",
		)
	else:
		st.caption("Saved sessions will appear here.")

with report_tab:
	st.subheader("Current session report")
	report = generate_report(score, level, recommendation).strip()
	st.code(report, language="text")
	st.download_button(
		"Download report",
		data=report,
		file_name="classroom-session-report.txt",
		mime="text/plain",
	)
