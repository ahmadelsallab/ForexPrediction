using System;
using System.Collections.Generic;
using System.Linq;
using System.Text;
using IronPython.Hosting;
using Microsoft.Scripting;
using System.Diagnostics;
using System.IO;
namespace SentimentPrediction
{
    class Program
    {
        static void RunCmd(string cmd, string args)
        {
            ProcessStartInfo start = new ProcessStartInfo();
            start.FileName = cmd;//cmd is full path to python.exe
            start.Arguments = args;//args is path to .py file and any cmd line args
            start.UseShellExecute = false;
            start.RedirectStandardOutput = true;
            using (Process process = Process.Start(start))
            {
                using (StreamReader reader = process.StandardOutput)
                {
                    string result = reader.ReadToEnd();
                    Console.Write(result);
                }
            }
        }

        static String PredictSentiment(string text)
        {
            ProcessStartInfo start = new ProcessStartInfo();
            start.FileName = @"c:\Python33\python.exe";
            start.Arguments = @"""C:\Users\ASALLAB\Google Drive\Guru_Forex\Code\forex\predict_text_sentiment.py"" " + text;//args is path to .py file and any cmd line args
            start.UseShellExecute = false;
            start.RedirectStandardOutput = true;
            using (Process process = Process.Start(start))
            {
                using (StreamReader reader = process.StandardOutput)
                {
                    String result = reader.ReadToEnd();
                    return result;
                }
            }
        }

        static void Main(string[] args)
        {
            //ScriptEngine engine = Python.CreateEngine();
            //engine.ExecuteFile(@"test.py");
            //string cmd = "c:\\Python33\\python.exe \"C:\\Users\\ASALLAB\\Google Drive\\Guru_Forex\\Code\\forex\\predict_text_sentiment.py\"";
            //Console.WriteLine(cmd);
            //Program.RunCmd(@"c:\\Python33\\python.exe ""C:\\Users\\ASALLAB\\Google Drive\\Guru_Forex\\Code\\forex\\predict_text_sentiment.py""", "Hello");
            //Program.RunCmd(@"c:\Python33\python.exe", @"""C:\Users\ASALLAB\Google Drive\Guru_Forex\Code\forex\predict_text_sentiment.py"" Hello");
            String headline = "Caterpillar down 0.8% to lead Dow decliners";
            String result = Program.PredictSentiment(headline);
            Console.WriteLine(result);
        }


    }
}
