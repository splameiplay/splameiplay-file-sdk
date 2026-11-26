/*  Copyright 2026 Splamei
 *
 *  Licensed under the Apache License, Version 2.0 (the "License");
 *  you may not use this file except in compliance with the License.
 *  You may obtain a copy of the License at
 *
 *      http://www.apache.org/licenses/LICENSE-2.0
 *
 *  Unless required by applicable law or agreed to in writing, software
 *  distributed under the License is distributed on an "AS IS" BASIS,
 *  WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
 *  See the License for the specific language governing permissions and
 *  limitations under the License.
 */

namespace SplameiPlay.SDK.Files;

internal static class Reader
{
    public static Dictionary<string, Dictionary<string, string>> readSyntax1_1(string[] lines)
    {
        bool selfThrow = false;
        Dictionary<string, Dictionary<string, string>> parsedFileData = new Dictionary<string, Dictionary<string, string>>();

        try
        {
            if (!string.IsNullOrEmpty(lines[3]))
            {
                selfThrow = true;
                throw new SplameiplayFiles.CustomFileSyntaxException($"Unable to read. Line 4 must be blank, yet is not.");
            }

            string currentSection = "Global";
            Dictionary<string, string> currentEntrys = new Dictionary<string, string>();
            List<string> passedSections = new List<string>() { "Global" };

            for (int i = 4; i < lines.Length; i++)
            {
                string currentLine = lines[i];
                if (currentLine.StartsWith("#"))
                {
                    continue;
                }
                else if (currentLine.StartsWith("/"))
                {
                    string sectionName = currentLine.Substring(1);
                    if (!Helpers.isValidKeySectionName(sectionName))
                    {
                        selfThrow = true;
                        throw new SplameiplayFiles.CustomFileSyntaxException($"Unable to read. The section name on line {i + 1} ({sectionName}) is invalid");
                    }
                    else if (passedSections.Contains(sectionName))
                    {
                        selfThrow = true;
                        throw new SplameiplayFiles.CustomFileSyntaxException($"Unable to read. The section '{sectionName}' was provided twice. This is not allowed");
                    }

                    parsedFileData.Add(currentSection, currentEntrys);
                    currentEntrys = new Dictionary<string, string>();
                    currentSection = sectionName;
                    passedSections.Add(sectionName);
                }
                else if (!string.IsNullOrEmpty(currentLine))
                {
                    string key = "";
                    string value = "";

                    if (currentLine.Contains("="))
                    {
                        (key, value) = Helpers.getKeyValueFromLine(currentLine);

                        if (Helpers.isValidKeySectionName(key))
                        {
                            currentEntrys.Add(key, Helpers.convertFakeToRealSpecialCharacters(value));
                        }
                        else
                        {
                            selfThrow = true;
                            throw new SplameiplayFiles.CustomFileSyntaxException($"Unable to read. The key name on line {i + 1} ({key}) is invalid.");
                        }
                    }
                    else
                    {
                        currentEntrys.Add(currentLine, string.Empty);
                    }
                }
            }

            parsedFileData.Add(currentSection, currentEntrys);

            return parsedFileData;
        }
        catch (Exception)
        {
            if (selfThrow)
            {
                throw;
            }

            throw new SplameiplayFiles.CustomFileParseException("Unable to read due to an unknown error. Is the data following the syntax?");
        }
    }
}