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

from typing import List
import re, os

from .Exceptions import CustomFileSyntaxException

class Helper:
    def getHeader(lines: List[str]) -> tuple[float, str, float]:
        fileVersion = 1; fileType = ""; fileTypeVersion = 1

        fileVersionStr = lines[0]
        fileTypeStr = lines[1]
        fileTypeVersionsStr = lines[2]

        fileVersion = float(fileVersionStr.split("=")[1])
        fileType = fileTypeStr.split("=")[1]
        fileTypeVersion = float(fileTypeVersionsStr.split("=")[1])

        return (fileVersion, fileType, fileTypeVersion)

    def isValidKeySectionName(name: str) -> bool:
        return re.match("^[a-zA-Z0-9_-]+$", name)

    def getKeyValueFromLine(line: str) -> tuple[str, str]:
        firstEqual = line.find("=")

        key = ""; value = ""

        if firstEqual == -1:
            key = line
        else:
            key = line[0:firstEqual]
            value = line[firstEqual + 1:]

        return (key, value)

    def convertFakeToRealSpecialCharacters(value: str) -> str:
        newLine = value.replace("\\n", "\n")
        reset = newLine.replace("\\r", "\r")

        return reset

    def checkFileExt(path: str):
        try:
            filename, fileExt = os.path.splitext(path)
            if fileExt != ".splameiplay" and fileExt != ".spinstaller" and fileExt != ".sptheme":
                raise CustomFileSyntaxException(f"Failed to use the file '{path}'. The file extension is not a valid extension.")
        except Exception:
            raise CustomFileSyntaxException(f"Unable to use the file. Failed to check the file extension for '{path}'")

    def convertKeyValueToFile(key: str, value: str) -> str:
        if (not value or value == ""):
            return key
        else:
            ogString = value
            ogString = ogString.replace("\n", "\\n")
            ogString = ogString.replace("\r", "\\r")

            return f"{key}={ogString}"