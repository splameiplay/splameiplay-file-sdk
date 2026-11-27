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
using System.Collections.Generic;
using System.IO;
using System.Reflection;

namespace SplameiPlay.SDK.Files
{
    public static class SplameiplayFiles
    {
        /// <summary>
        /// The version of the SplameiPlay File SDK
        /// </summary>
        public static Version version { get; } = Assembly.GetExecutingAssembly().GetName().Version;

        /// <summary>
        /// Determains if the SplameiPlay File SDK is a pre-release version
        /// </summary>
        public static bool isPreRelease { get; } = true;

        /// <summary>
        /// The platform this version is built for
        /// </summary>
        public static string platform { get; } = ".NET Framework";

        /// <summary>
        /// Simple marco polo repeater. Use to verify the SDK is working
        /// </summary>
        /// <returns>Returns 'Polo!' and nothing else</returns>
        public static string Marco()
        {
            return "Polo!";
        }

        /// <summary>
        /// Checks if the SDK is a debug (pre-release) version
        /// </summary>
        /// <returns>Returns true if built as debug, false if built as release</returns>
        public static bool IsDebug()
        {
#if DEBUG
            return true;
#else
            return false;
#endif
        }

        #region Exceptions

        public class CustomFileReadException : Exception
        {
            public CustomFileReadException(string message) : base(message) { }
        }

        public class CustomFileParseException : Exception
        {
            public CustomFileParseException(string message) : base(message) { }
        }

        public class CustomFileSyntaxException : Exception
        {
            public CustomFileSyntaxException(string message) : base(message) { }
        }

        public class CustomFileSaveException : Exception
        {
            public CustomFileSaveException(string message) : base(message) { }
        }

        #endregion

        #region Public data

        public struct SplameiplayFileData
        {
            public float fileVersion;
            public string type;
            public float typeVersion;

            public Dictionary<string, Dictionary<string, string>> data;
        }

        #endregion

        #region Public functions

        /// <summary>
        /// Reads a SplameiPlay file from disk and returns it's parsed content
        /// </summary>
        /// <param name="filePath">The full path on disk of the file</param>
        /// <param name="checkFileExt">Sets if the SDK should check the file extension before reading. Default: true</param>
        /// <returns>The parsed content of the SplameiPlay file</returns>
        /// <exception cref="CustomFileReadException"></exception>
        /// <exception cref="CustomFileSyntaxException"></exception>
        /// <exception cref="CustomFileParseException"></exception>
        public static SplameiplayFileData ReadFile(string filePath, bool checkFileExt = true)
        {
            string[] lines = new string[0];
            bool selfThrow = false;

            try
            {
                string fullFilePath = Path.GetFullPath(filePath);
                lines = File.ReadAllLines(fullFilePath);

                if (checkFileExt)
                {
                    selfThrow = true;
                    Helpers.checkFileExt(fullFilePath);
                    selfThrow = false;
                }
            }
            catch (Exception)
            {
                if (selfThrow)
                {
                    throw;
                }
                throw new CustomFileReadException($"Failed to read '{filePath}'. Is the file accessable by the SDK and does it exists?");
            }

            return ReadData(lines);
        }

        /// <summary>
        /// Reads the raw content of a SplameiPlay File from memory (an array) instead of from disk
        /// </summary>
        /// <param name="splameiplayData">The content of the file, where each entry in the array is a new line</param>
        /// <returns>The parsed content of the SplameiPlay file</returns>
        /// <exception cref="CustomFileReadException"></exception>
        /// <exception cref="CustomFileSyntaxException"></exception>
        /// <exception cref="CustomFileParseException"></exception>
        public static SplameiplayFileData ReadData(string[] splameiplayData)
        {
            string[] lines = splameiplayData;

            float fileVersion; string fileType; float fileTypeVersion;

            try
            {
                (fileVersion, fileType, fileTypeVersion) = Helpers.getHeader(lines);
            }
            catch (Exception)
            {
                throw new CustomFileReadException("Unable to read the header. Is it following the syntax?");
            }

            Dictionary<string, Dictionary<string, string>> parsedData = new Dictionary<string, Dictionary<string, string>>();
            SplameiplayFileData result = new SplameiplayFileData();

            if (fileVersion == 1.1f)
            {
                parsedData = Reader.readSyntax1_1(lines);
            }
            else
            {
                throw new CustomFileParseException($"Unable to read the file. The file version '{fileVersion}' is not supported by this version of the SDK");
            }

            result.fileVersion = fileVersion;
            result.type = fileType;
            result.typeVersion = fileTypeVersion;

            result.data = parsedData;

            return result;
        }

        /// <summary>
        /// Saves content to a SplameiPlay file on disk with the set metadata
        /// </summary>
        /// <param name="filePath">The path to save the file to</param>
        /// <param name="type">The type of file</param>
        /// <param name="typeVersion">The version of the type</param>
        /// <param name="data">The data of the SplameiPlay file</param>
        /// <param name="checkFileExt">Sets if the file extension should be checked before doing anything. Default: true</param>
        /// <param name="allowEqualSignsInContentValues">Sets if saving SplameiPlay files with an equal sign in the content should be allowed. This is known to sometime cause issues. Default: true</param>
        /// <param name="fileVersion">The specific version of the SplameiPlay file syntax to use. Default: 1.1</param>
        /// <exception cref="CustomFileReadException"></exception>
        /// <exception cref="CustomFileSyntaxException"></exception>
        /// <exception cref="CustomFileParseException"></exception>
        public static void SaveFile(string filePath, string type, float typeVersion, Dictionary<string, Dictionary<string, string>> data, bool checkFileExt = true, bool allowEqualSignsInContentValues = true, float fileVersion = 1.1f)
        {
            bool selfThrow = false;
            string fullFilePath;

            try
            {
                fullFilePath = Path.GetFullPath(filePath);

                if (checkFileExt)
                {
                    selfThrow = true;
                    Helpers.checkFileExt(fullFilePath);
                    selfThrow = false;
                }
            }
            catch (Exception)
            {
                if (selfThrow)
                {
                    throw;
                }
                throw new CustomFileReadException($"Failed to use '{filePath}'. Is it a valid path?");
            }

            string compiledData;
            switch (fileVersion)
            {
                case 1.1f:
                    compiledData = Writer.writeSyntax1_1(type, typeVersion, data, allowEqualSignsInContentValues);
                    break;
                default:
                    throw new CustomFileParseException($"Failed to save the file. File version '{fileVersion}' is not supported by this version of the SDK");
            }

            File.WriteAllText(fullFilePath, compiledData);
        }

        /// <summary>
        /// Saves content to a SplameiPlay file to memory (string) with the set metadata
        /// </summary>
        /// <param name="type">The type of file</param>
        /// <param name="typeVersion">The version of the type</param>
        /// <param name="data">The data of the SplameiPlay file</param>
        /// <param name="allowEqualSignsInContentValues">Sets if saving SplameiPlay files with an equal sign in the content should be allowed. This is known to sometime cause issues. Default: true</param>
        /// <param name="fileVersion">The specific version of the SplameiPlay file syntax to use. Default: 1.1</param>
        /// <returns>The resulting SplameiPlay file as a string</returns>
        /// <exception cref="CustomFileReadException"></exception>
        /// <exception cref="CustomFileSyntaxException"></exception>
        /// <exception cref="CustomFileParseException"></exception>
        public static string SaveData(string type, float typeVersion, Dictionary<string, Dictionary<string, string>> data, bool allowEqualSignsInContentValues = true, float fileVersion = 1.1f)
        {
            switch (fileVersion)
            {
                case 1.1f:
                    return Writer.writeSyntax1_1(type, typeVersion, data, allowEqualSignsInContentValues);
                default:
                    throw new CustomFileParseException($"Failed to save the file. File version '{fileVersion}' is not supported by this version of the SDK");
            }
        }

        #endregion
    }
}
