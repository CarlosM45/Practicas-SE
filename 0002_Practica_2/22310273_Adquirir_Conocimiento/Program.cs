using System;
using System.Collections.Generic;
using System.IO;

class Chatbot
{
    static Dictionary<string, string> knowledgeBase = new Dictionary<string, string>();
    const string filePath = "knowledge.txt";

    static void Main()
    {
        LoadKnowledge();

        while (true)
        {
            Console.Write("Usuario: ");
            string question = Console.ReadLine()?.Trim().ToLower();

            if (string.IsNullOrEmpty(question)) continue;

            if (knowledgeBase.ContainsKey(question))
            {
                Console.WriteLine("Bot: " + knowledgeBase[question]);
            }
            else
            {
                Console.Write("Bot: No sé cómo responder. ¿Qué debería decir? ");
                string answer = Console.ReadLine()?.Trim();
                if (!string.IsNullOrEmpty(answer))
                {
                    knowledgeBase[question] = answer;
                    SaveKnowledge(question, answer);
                    Console.WriteLine("Bot: ¡Gracias! Lo recordaré.");
                }
            }
        }
    }

    static void LoadKnowledge()
    {
        if (!File.Exists(filePath)) return;

        foreach (var line in File.ReadAllLines(filePath))
        {
            var parts = line.Split('|');
            if (parts.Length == 2)
                knowledgeBase[parts[0]] = parts[1];
        }
    }

    static void SaveKnowledge(string question, string answer)
    {
        using (StreamWriter sw = File.AppendText(filePath))
        {
            sw.WriteLine($"{question}|{answer}");
        }
    }
}
