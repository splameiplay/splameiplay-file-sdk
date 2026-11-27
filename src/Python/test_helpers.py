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

from SplameiPlay_File_SDK._Helper import Helper
import SplameiPlay_File_SDK
import pytest

def test_header():
    lines = ["Version=1.1", "Type=Hello", "TypeVersion=1.2"]
    fileVersion, fileType, fileTypeVersion = Helper.getHeader(lines)

    assert fileVersion == 1.1
    assert fileType == "Hello"
    assert fileTypeVersion == 1.2

def test_invalid_header():
    try:
        lines = ["Version=1.1e", "Type=Hello", "TypeVersion=1.2"]
        Helper.getHeader(lines)

        pytest.fail("The invalid header was accepted but doesn't follow the syntax! (Invalid Version=)")
    except ValueError:
        print("Test one pass!")

    try:
        lines = ["Version=1.1", "TypeVersion=1.2"]
        Helper.getHeader(lines)

        pytest.fail("The invalid header was accepted but doesn't follow the syntax! (Missing Type=)")
    except IndexError:
        print("Test two pass!")

def test_invalid_key_section_name():
    sectionName = "HelloWorld"
    assert Helper.isValidKeySectionName(sectionName)

    sectionName = "Hello World"
    assert not Helper.isValidKeySectionName(sectionName)

    sectionName = "Hello World @"
    assert not Helper.isValidKeySectionName(sectionName)

def test_get_key_value():
    line = "Hello=World"
    key, value = Helper.getKeyValueFromLine(line)
    assert key == "Hello" and value == "World"

    line = "Hello"
    key, value = Helper.getKeyValueFromLine(line)
    assert key == "Hello" and value == ""

    line = "Hello="
    key, value = Helper.getKeyValueFromLine(line)
    assert key == "Hello" and value == ""

def test_special_character_convert():
    value = "Hello\\nWorld\\r"
    result = Helper.convertFakeToRealSpecialCharacters(value)
    assert result == "Hello\nWorld\r"

    value = "Hello World\\n\\r"
    result = Helper.convertFakeToRealSpecialCharacters(value)
    assert result == "Hello World\n\r"

    value = "Hello World"
    result = Helper.convertFakeToRealSpecialCharacters(value)
    assert result == "Hello World"

def test_file_ext_check():
    filename = "hello.splameiplay"
    Helper.checkFileExt(filename)

    filename = "hello.spinstaller"
    Helper.checkFileExt(filename)

    filename = "hello.sptheme"
    Helper.checkFileExt(filename)

    try:
        filename = "hello.world"
        Helper.checkFileExt(filename)

        pytest.fail(f"'{filename}' was accepted but shouldn't be!")
    except SplameiPlay_File_SDK.CustomFileSyntaxException:
        print("Test four pass!")

def test_key_value_str_conversion():
    result = Helper.convertKeyValueToFile("Hello", "World")
    assert result == "Hello=World"

    result = Helper.convertKeyValueToFile("Hello", "World\nHi")
    assert result == "Hello=World\\nHi"

    result = Helper.convertKeyValueToFile("Hello", "")
    assert result == "Hello"