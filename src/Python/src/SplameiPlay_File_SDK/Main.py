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
from ._Helper import Helper
from ._Reader import Reader
from ._Writer import Writer
from .Exceptions import CustomFileSyntaxException, CustomFileParseException, CustomFileReadException

def is_pre_release() -> bool:
    """Determains if the SplameiPlay File SDK is a pre-release version

    Returns:
        True if a pre-release version - False if a release version
    """

    return True;

def get_platform() -> str:
    """The platform this version is built for

    Returns:
        This value is always 'Python'
    """
    return "Python"

def marco() -> str:
    """Simple marco polo repeater. Use to verify the SDK is working

    Returns:
        Returns 'Polo!'. That's it...
    """

    return "Polo!"

class SplameiPlay_File_Data():
    def __init__(self, file_version, file_type, file_type_version, data):
        self.file_version = file_version
        self.file_type = file_type
        self.file_type_version = file_type_version

        self.data = data

def read_splameiplay_data(splameiplayData: List[str]) -> SplameiPlay_File_Data:
    """Reads the raw content of a SplameiPlay File from memory (an string list)

    Args:
        splameiplayData: The content of the file, where each entry in the array is a new line

    Returns:
        The parsed content of the SplameiPlay file

    Raises:
        CustomFileReadException
        CustomFileSyntaxException
        CustomFileParseException
    """

    lines = splameiplayData

    fileVersion = 1.0; fileType = ""; fileTypeVersion = 1.0

    try:
        fileVersion, fileType, fileTypeVersion = Helper.getHeader(lines)
    except Exception:
        raise CustomFileReadException("Unable to read the header. Is it following the syntax?")

    if not Helper.isValidKeySectionName(fileType):
        raise CustomFileSyntaxException(f"Unable to read. The type name ({fileType}) is invalid")

    parsedData = {}

    if fileVersion == 1.1:
        parsedData = Reader.readSyntax1_1(lines)
    else:
        raise CustomFileParseException(f"Unable to read the file. The file version '{fileVersion}' is not compatible with this version of the SDK")

    result = SplameiPlay_File_Data(file_version=fileVersion,
                                 file_type=fileType,
                                 file_type_version=fileTypeVersion,
                                 
                                 data=parsedData)

    return result

def save_splameiplay_data(type: str, typeVersion: float, data: dict[str, dict[str, str]], allowEqualSignsInContentValues: bool = True, fileVersion: float = 1.1) -> str:
    writer = Writer()
    
    if fileVersion == 1.1:
        return writer.writeSyntax1_1(type, typeVersion, data, allowEqualSignsInContentValues)
    else:
        raise CustomFileParseException(f"Failed to save the file. File version '{fileVersion}' is not supported by this version of the SDK")