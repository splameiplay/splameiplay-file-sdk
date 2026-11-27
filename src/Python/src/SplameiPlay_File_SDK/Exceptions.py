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

class CustomFileSyntaxException(Exception):
    """Raised when the file your trying to read/save is invalid (doesn't follow the syntax)"""
    def __init__(self, message):
        super().__init__(message)

class CustomFileParseException(Exception):
    """Raised when an error occurs when trying to read/save your file. This is often a generic catch-all error and doesn't always pin-point a expecific issue"""
    def __init__(self, message):
        super().__init__(message)

class CustomFileReadException(Exception):
    """Raised when an error occurs trying to read a file. Currently, unlike other versions of the SDK, this is only thrown when an error occured reading the header"""
    def __init__(self, message):
        super().__init__(message)