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
from .Exceptions import CustomFileSyntaxException, CustomFileParseException

from ._Helper import Helper

class Reader:
    def readSyntax1_1(lines: List[str]) -> dict[str, dict[str]]:
        selfThrow = False
        parsedFileData = {}

        try:
            if lines[3] != "":
                selfThrow = True
                raise CustomFileSyntaxException("Unable to read. Line 4 must be blank, yet is not.")

            currentSection = "Global"
            currentEntrys = {}
            passedSections = ["Global"]

            i = 4
            for x in range(len(lines) - 4):
                currentLine = lines[i]

                if currentLine.startswith("#"):
                    continue;
                
                elif currentLine.startswith("/"):
                    sectionName = currentLine[1:]

                    if not Helper.isValidKeySectionName(sectionName):
                        selfThrow = True
                        raise CustomFileSyntaxException(f"Unable to read. The section name on line {i + 1} ({sectionName}) is invalid")
                    elif sectionName in passedSections:
                        selfThrow = True
                        raise CustomFileSyntaxException(f"Unable to read. The section '{sectionName}' was provided twice. This is not allowed")

                    parsedFileData[currentSection] = currentEntrys
                    currentEntrys = {}
                    currentSection = sectionName
                    passedSections.append(sectionName)

                elif currentLine != "":
                    key = ""
                    value = ""

                    if "=" in currentLine:
                        (key, value) = Helper.getKeyValueFromLine(currentLine)

                        if Helper.isValidKeySectionName(key):
                            currentEntrys[key] = Helper.convertFakeToRealSpecialCharacters(value)
                        else:
                            selfThrow = True
                            raise CustomFileSyntaxException(f"Unable to read. The key name on line {i + 1} ({key}) is invalid.")

                    else:
                        currentEntrys[currentLine] = ""

                i += 1

            parsedFileData[currentSection] = currentEntrys

            return parsedFileData

        except Exception:
            if selfThrow:
                raise

            raise CustomFileParseException(f"Unable to read due to an unknown error. Is the data following the syntax?")