from assistant.rules import reply


def test_greeting():
    assert "Hello" in reply("hi")


def test_office_lookup():
    assert "I.101" in reply("Where is the Training Office?")
    assert "A.002" in reply("Where is the Accounting Office?")
    assert "A.001" in reply("Where is the Admissions Office?")

def test_new_offices_lookup():
    assert "A.002" in reply("Where is the Accounting Office?")
    assert "A.001" in reply("Where is the Admissions Office?")


def test_unknown():
    assert "don't know" in reply("what is the meaning of life")


def test_empty():
    assert reply("   ") == "Please type a question."
