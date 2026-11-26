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

using System.Globalization;

namespace SplameiPlay.SDK.Files;

internal class Writer
{
    public static string writeSyntax1_1(string type, float typeVersion, Dictionary<string, Dictionary<string, string>> data, bool allowEqualSignsInContentValues = true)
    {
        bool selfThrow = false;

        if (!Helpers.isValidKeySectionName(type))
        {
            throw new SplameiplayFiles.CustomFileSyntaxException($"Unable to write the file. The type ({type}) is invalid.");
        }

        List<string> fileData = new List<string>() { "Version=1.1", $"Type={type}", $"TypeVersion={typeVersion.ToString(".0", CultureInfo.InvariantCulture)}", "" };

        try
        {
            var globalData = data["Global"];
            fileData = convertRawToContent(globalData, "Global", allowEqualSignsInContentValues, fileData);

            foreach (var section in data)
            {
                if (section.Key == "Global") { continue; }

                if (!Helpers.isValidKeySectionName(section.Key))
                {
                    selfThrow = true;
                    throw new SplameiplayFiles.CustomFileSyntaxException($"Unable to write the file. The section name '{section.Key}' is invalid");
                }

                fileData.Add(""); fileData.Add($"/{section.Key}"); fileData.Add("");

                var sectionData = section.Value;
                fileData = convertRawToContent(sectionData, section.Key, allowEqualSignsInContentValues, fileData);
            }

            return string.Join("\n", fileData);
        }
        catch (Exception)
        {
            if (selfThrow)
            {
                throw;
            }

            throw new SplameiplayFiles.CustomFileParseException($"Unable to write the file. Does the provided data have the correct syntax?");
        }
    }

    internal static List<string> convertRawToContent(Dictionary<string, string> sectionData, string section, bool allowEqualSignsInContentValues, List<string> currentFileData)
    {
        foreach (var sectionlDataValue in sectionData)
        {
            if (!Helpers.isValidKeySectionName(sectionlDataValue.Key))
            {
                throw new SplameiplayFiles.CustomFileSyntaxException($"Unable to write the file. The key '{sectionlDataValue.Key}' from section '{section}' is invalid");
            }
            else
            {
                if (!allowEqualSignsInContentValues)
                {
                    if (sectionlDataValue.Value.Contains("="))
                    {
                        throw new SplameiplayFiles.CustomFileSyntaxException($"Unable to write the file. A content value contains an equal sign (=) and we we're told to disallow it. Content: {sectionlDataValue.Value}");
                    }
                }

                string addingData = Helpers.convertKeyValueToFile(sectionlDataValue.Key, sectionlDataValue.Value);
                currentFileData.Add(addingData);
            }
        }

        return currentFileData;
    }
}