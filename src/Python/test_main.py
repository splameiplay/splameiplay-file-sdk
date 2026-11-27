"""Copyright 2026 Splamei

 Licensed under the Apache License, Version 2.0 (the "License");
 you may not use this file except in compliance with the License.
 You may obtain a copy of the License at

    http://www.apache.org/licenses/LICENSE-2.0

 Unless required by applicable law or agreed to in writing, software
 distributed under the License is distributed on an "AS IS" BASIS,
 WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
 See the License for the specific language governing permissions and
 limitations under the License."""

import SplameiPlay_File_SDK, pytest

def test_splameiplay_read():
    payload = ["Version=1.1", "Type=Hello", "TypeVersion=1.1", "", "Hello=World", "Hi", "/Section", "Key=Line\\nValue"]
    result = SplameiPlay_File_SDK.read_splameiplay_data(payload)

    assert result.file_version == 1.1
    assert result.file_type == "Hello"
    assert result.file_type_version == 1.1

    data = result.data

    globalSection = data["Global"]
    assert globalSection["Hello"] == "World"
    assert globalSection["Hi"] == ""

    sectionSection = data["Section"]
    assert sectionSection["Key"] == "Line\nValue"

def test_splameiplay_read_failure():
    payload = ["Version=1.1", "Type=Hello", "TypeVersion=1.1", "", "Hello=World", "Hi", "/Section", "Key=Line\\nValue"]

    try:
        payload[0] = "Version=1.0"
        SplameiPlay_File_SDK.read_splameiplay_data(payload)
        pytest.fail("Accepted the new payload (file) despite the version being invalid!")
    except Exception:
        print("Test one pass!")

    try:
        payload[0] = "Version=1.1"
        payload[1] = "Type=Hello Hi"
        print(payload)
        SplameiPlay_File_SDK.read_splameiplay_data(payload)
        pytest.fail("Accepted the new payload (file) despite the type being invalid!")
    except Exception:
        print("Test two pass!")

    try:
        payload[1] = "Type=Hello"
        payload[2] = "TypeVersion=Hi"
        SplameiPlay_File_SDK.read_splameiplay_data(payload)
        pytest.fail("Accepted the new payload (file) despite the type version being invalid!")
    except Exception:
        print("Test three pass!")

    try:
        payload[2] = "TypeVersion=1.1"
        payload.append("Hello World=Hi")
        SplameiPlay_File_SDK.read_splameiplay_data(payload)
        pytest.fail("Accepted the new payload (file) despite the a key being invalid!")
    except Exception:
        print("Test four pass!")

    try:
        payload[8] = "/Hello World"
        SplameiPlay_File_SDK.read_splameiplay_data(payload)
        pytest.fail("Accepted the new payload (file) despite the a section being invalid!")
    except Exception:
        print("Test five pass!")

def test_splameiplay_save():
    type = "Hello"
    typeVersion = 1.1
    payload = {"Global": {"Hello": "World", "Hi": ""}, "Section": {"Key": "Line\nValue"}}
    expectedResult = """Version=1.1
Type=Hello
TypeVersion=1.1

Hello=World
Hi

/Section

Key=Line\\nValue"""

    result = SplameiPlay_File_SDK.save_splameiplay_data(type, typeVersion, payload)

    assert result == expectedResult

def test_splameiplay_save_failure():
    type = "Hello"
    typeVersion = 1.1
    payload = {"Global": {"Hello": "World", "Hi": ""}, "Section": {"Key": "Line\nValue"}}

    try:
        payload["NewSection"] = {"Key": "Hello=World"}

        SplameiPlay_File_SDK.save_splameiplay_data(type, typeVersion, payload, allowEqualSignsInContentValues=False)
        pytest.fail("Accepted the new payload (file) despite being told to disallow equal signs!")
    except Exception:
        print("Test one pass!")

    try:
        payload["NewSection2"] = {"Hello World": "Hello World"}

        SplameiPlay_File_SDK.save_splameiplay_data(type, typeVersion, payload)
        pytest.fail("Accepted the new payload (file) despite having an invalid key!")
    except Exception:
        print("Test two pass!")

    type = "Hello World"
    try:
        payload["NewSection2"] = {"Key": "Hello=World"}

        SplameiPlay_File_SDK.save_splameiplay_data(type, typeVersion, payload)
        pytest.fail("Accepted the new payload (file) despite having an invalid type!")
    except Exception:
        print("Test three pass!")