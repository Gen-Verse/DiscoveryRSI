from discovery_rsi.providers import _stream_text, CodexAdapter, ClaudeCodeAdapter

def test_stream_text_uses_final_result():
    assert _stream_text('{"type":"assistant","message":{"content":[{"type":"text","text":"draft"}]}}\n{"type":"result","result":"final"}') == "final"

def test_native_command_shapes():
    assert CodexAdapter(model="demo").sandbox == "read-only"
    assert ClaudeCodeAdapter(agent="lead").agent == "lead"
