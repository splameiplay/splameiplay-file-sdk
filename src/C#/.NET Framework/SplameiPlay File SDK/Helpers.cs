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

using System;
using System.Globalization;
using System.IO;
using System.Text.RegularExpressions;

namespace SplameiPlay.SDK.Files
{
    internal static class Helpers
    {
        public static (float, string, float) getHeader(string[] lines)
        {
            float fileVersion; string fileType; float fileTypeVersion;

            string fileVersionStr = lines[0];
            string fileTypeStr = lines[1];
            string fileTypeVersionStr = lines[2];

            fileVersion = float.Parse(fileVersionStr.Split('=')[1], CultureInfo.InvariantCulture);
            fileType = fileTypeStr.Split('=')[1];
            fileTypeVersion = float.Parse(fileTypeVersionStr.Split('=')[1], CultureInfo.InvariantCulture);

            return (fileVersion, fileType, fileTypeVersion);
        }

        public static bool isValidKeySectionName(string name)
        {
            return Regex.IsMatch(name, @"^[a-zA-Z0-9_-]+$");
        }

        public static (string, string) getKeyValueFromLine(string line)
        {
            int firstEqual = line.IndexOf('=');

            string key;
            string value;

            if (firstEqual == -1)
            {
                key = line;
                value = string.Empty;
            }
            else
            {
                key = line.Substring(0, firstEqual);
                value = line.Substring(firstEqual + 1);
            }

            return (key, value);
        }

        public static string convertFakeToRealSpecialCharacters(string value)
        {
            string newLine = value.Replace(@"\n", "\n");
            string reset = newLine.Replace(@"\r", "\r");

            return reset;
        }

        public static void checkFileExt(string path)
        {
            try
            {
                string fileExt = Path.GetExtension(path);
                if (fileExt != ".splameiplay" && fileExt != ".spinstaller" && fileExt != ".sptheme")
                {
                    throw new SplameiplayFiles.CustomFileSyntaxException($"Failed to use the file '{path}'. The file extension is not a valid extension.");
                }
            }
            catch (Exception)
            {
                throw new SplameiplayFiles.CustomFileSyntaxException($"Unable to use the file. Failed to check the file extension for '{path}'");
            }
        }

        public static string convertKeyValueToFile(string key, string value)
        {
            if (string.IsNullOrEmpty(value))
            {
                return key;
            }
            else
            {
                string ogString = value;
                ogString = ogString.Replace("\n", @"\n");
                ogString = Regex.Replace(ogString, @"\t|\n|\r", "");
                return $"{key}={ogString}";
            }
        }
    }
}
