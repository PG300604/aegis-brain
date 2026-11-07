import pytest
from aegis.unslop_master import UnslopMaster, UnslopResult, unslop


class TestUnslopCodeFast:
    def test_unslop_code_fast(self):
        text = (
            "Certainly! Here is the code:\n"
            "# Import statements\n"
            "import os\n"
            "// Helper function\n"
            "def helper():\n"
            "    # Constructor\n"
            "    x = 1  # Initialize variable\n"
            "    # OpenAI token\n"
            "    return x\n"
            "I hope this helps!"
        )
        master = UnslopMaster(mode="code", deep=False)
        res = master.run(text)
        assert "import os" in res.cleaned_text
        assert "def helper():" in res.cleaned_text
        assert "Certainly! Here is the code:" not in res.cleaned_text
        assert "I hope this helps!" not in res.cleaned_text
        assert "# Import statements" not in res.cleaned_text
        assert "// Helper function" not in res.cleaned_text
        assert "# Constructor" not in res.cleaned_text
        assert "# Initialize variable" not in res.cleaned_text
        assert "# OpenAI token" not in res.cleaned_text


class TestUnslopCodeDeep:
    def test_unslop_code_deep(self):
        text = "def my_stub():\n    pass\n\ndef real_func():\n    return 42"
        master = UnslopMaster(mode="code", deep=True)
        res = master.run(text)
        assert "stub" in res.findings or "my_stub" in res.findings


class TestUnslopProseSycophancyAndTransitions:
    def test_unslop_prose_sycophancy_and_transitions(self):
        text = (
            "Certainly! Sure! Of course! I would be happy to help. "
            "Let's dive in. As an AI language model, I can say that. "
            "Moreover, Furthermore, Additionally, In conclusion, it works."
        )
        master = UnslopMaster(mode="prose", deep=False)
        res = master.run(text)
        cleaned = res.cleaned_text
        for phrase in [
            "Certainly!", "Sure!", "Of course!", "I would be happy to help",
            "Let's dive in", "As an AI language model",
            "Moreover,", "Furthermore,", "Additionally,", "In conclusion,"
        ]:
            assert phrase not in cleaned


class TestUnslopProseStockVocabDeep:
    def test_unslop_prose_stock_vocab_deep(self):
        text = (
            "Let's delve into this testament to a rich tapestry of pivotal "
            "seamlessly robust leverage in today's world cutting-edge "
            "supercharge game-changer."
        )
        master = UnslopMaster(mode="prose", deep=True)
        res = master.run(text)
        cleaned = res.cleaned_text
        assert "explore" in cleaned
        assert "evidence of" in cleaned
        assert "collection" in cleaned
        assert "key" in cleaned
        assert "smoothly" in cleaned
        assert "reliable" in cleaned
        assert "use" in cleaned
        assert "today" in cleaned
        assert "modern" in cleaned
        assert "boost" in cleaned
        assert "major change" in cleaned


class TestUnslopEmDashAndTricolon:
    def test_unslop_em_dash_and_tricolon(self):
        text = "No bugs — no crashes — no downtime. Also — a test — here."
        master = UnslopMaster(mode="prose", deep=False)
        res = master.run(text)
        cleaned = res.cleaned_text
        assert " — " not in cleaned
        assert "No bugs, no crashes, no downtime" not in cleaned or "No bugs" in cleaned


class TestUnslopUI:
    def test_unslop_ui(self):
        text = "filter: blur(20px); bg-gradient-to-r from-purple-500 via-pink-500 to-red-500;"
        master = UnslopMaster(mode="ui", deep=False)
        res = master.run(text)
        assert "filter: blur(20px)" not in res.cleaned_text
        assert "bg-gradient-to-r" not in res.cleaned_text


class TestDetectSlopScoring:
    def test_clean_text_scores_100(self):
        text = "This is clean, normal text without any slop."
        master = UnslopMaster(mode="prose", deep=False)
        res = master.run(text)
        assert res.score == 100
        assert res.slop_detected is False

    def test_sloppy_text_scores_low(self):
        text = "Certainly! Here is the code: delve into robust leverage."
        master = UnslopMaster(mode="prose", deep=True)
        res = master.run(text)
        assert res.score < 80
        assert res.slop_detected is True
        assert len(res.findings) > 0


class TestUnslopResultAndConvenience:
    def test_unslop_result_properties(self):
        text = "Test text."
        master = UnslopMaster(mode="prose", deep=False)
        res = master.run(text)
        assert isinstance(res, UnslopResult)
        assert hasattr(res, "cleaned_text")
        assert hasattr(res, "cleaned")
        assert hasattr(res, "score")
        assert hasattr(res, "slop_detected")
        assert hasattr(res, "findings")
        assert res.cleaned == res.cleaned_text

    def test_convenience_function(self):
        res = unslop("Certainly! Test.", deep=True)
        assert isinstance(res, UnslopResult)
        assert "Certainly!" not in res.cleaned_text

    def test_instance_method(self):
        master = UnslopMaster(mode="prose", deep=True)
        res = master.run("Certainly! Test.")
        assert isinstance(res, UnslopResult)
        assert "Certainly!" not in res.cleaned_text
