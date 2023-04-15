from pathlib import Path

current_dir = Path(__file__).parent.resolve()
server_dir = current_dir.parent.parent

F1_session1 = server_dir /  "F" / "F01" / "Session1"
F3_session1 = server_dir /  "F" / "F03" / "Session1"
F3_session2 = server_dir /  "F" / "F03" / "Session2"
F3_session3 = server_dir /  "F" / "F03" / "Session3"
F4_session1 = server_dir /  "F" / "F04" / "Session1"
F4_session2 = server_dir /  "F" / "F04" / "Session2"

FC1_session1 = server_dir /  "FC" / "FC01" / "Session1"
FC2_session2 = server_dir /  "FC" / "FC02" / "Session2"
FC2_session3 = server_dir /  "FC" / "FC02" / "Session3"
FC3_session1 = server_dir /  "FC" / "FC03" / "Session1"
FC3_session2 = server_dir /  "FC" / "FC03" / "Session2"


for session_path in [F1_session1, F3_session1, F3_session2, F3_session3, F4_session1, F4_session2, FC1_session1, FC2_session2, FC2_session3, FC3_session1, FC3_session2]:
    prompt_path = session_path / "prompts"
    prompt_files = list(prompt_path.glob("*.*"))

    prompts = [x.read_text() for x in prompt_files]

    for i, p in enumerate(prompts):
        if "xxx" in p:
            print(p.strip(), prompt_files[i])

