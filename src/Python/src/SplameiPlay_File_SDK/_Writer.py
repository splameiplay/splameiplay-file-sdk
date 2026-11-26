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

class Writer:
    def _convertRawToContent(self, sectionData: dict[str, str], section: str, allowEqualSignsInContentValues: bool, currentFileData: List[str]) -> List[str]:
            for sectionDataValue in sectionData.keys():
                key = sectionDataValue
                value = sectionData[key]
    
                if not Helper.isValidKeySectionName(key):
                    raise CustomFileSyntaxException(f"Unable to write the file. The key '{key}' from section '{section}' is invalid")
    
                else:
                    if not allowEqualSignsInContentValues:
                        if "=" in value:
                            raise CustomFileSyntaxException(f"Unable to write the file. A content value contains an equal sign (=) and we we're told to disallow it. Content: {value}")
    
                    addingData = Helper.convertKeyValueToFile(key, value)
                    currentFileData.append(addingData)
    
            return currentFileData
    
    def writeSyntax1_1(self, fileType: str, typeVersion: float, data: dict[str, dict[str, str]], allowEqualSignsInContentValues: bool = True) -> str:
        selfThrow = False

        if not Helper.isValidKeySectionName(fileType):
            raise CustomFileSyntaxException(f"Unable to write the file. The type ({type}) is invalid.")

        fileData = [ "Version=1.1", f"Type={fileType}", f"TypeVersion={str(typeVersion)}", "" ]

        try:
            globalData = data["Global"]
            fileData = self._convertRawToContent(globalData, "Global", allowEqualSignsInContentValues, fileData)

            for section in data.keys():
                key = section
                value = data[key]

                if key == "Global":
                    continue

                if not Helper.isValidKeySectionName(key):
                    selfThrow = True
                    raise CustomFileSyntaxException(f"Unable to write the file. The section name '{section.Key}' is invalid")

                fileData.append(""); fileData.append(f"/{key}"); fileData.append("")

                sectionData = value
                fileData = self._convertRawToContent(sectionData, key, allowEqualSignsInContentValues, fileData)

            return "\n".join([i for i in fileData[0:]])

        except Exception:
            if selfThrow:
                raise

            raise CustomFileParseException("Unable to write the file. Does the provided data have the correct syntax?")