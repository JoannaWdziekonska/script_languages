import json
import urllib.request


class MyDictionary:
    def __init__(self):
        self.phonetics = None
        self.parts_of_speech = None
        self.sound = None
        self.view = 0
        self.optional_germ_synonyms = None

    def search(self, word, language):
        url = "https://api.dictionaryapi.dev/api/v2/entries/{}/{}"
        data = urllib.request.urlopen(url.format(language, word)).read()

        output_json = json.loads(data)
        word_res = output_json[0]  # most common result

        parts_of_speech = {}
        for part_of_speech in word_res["meanings"]:
            parts_of_speech[part_of_speech["partOfSpeech"]] = part_of_speech["definitions"]

        if language != "de":
            self.sound = word_res["phonetics"][0]["audio"]
        self.phonetics = word_res["phonetics"][0]["text"]
        self.parts_of_speech = parts_of_speech

        if language == "de":
            germ_url = "https://dictionary.yandex.net/api/v1/dicservice.json/lookup?key=<keyhere>&lang=de-en&text={} "
            german_data = urllib.request.urlopen(germ_url.format(word)).read()
            german_output_json = json.loads(german_data)
            self.phonetics = "/" + german_output_json["def"][0]["ts"][1:] + "/"

            germ_synonyms = []
            if "mean" in german_output_json["def"][0]["tr"][0].keys():
                for i in german_output_json["def"][0]["tr"][0]["mean"]:
                    germ_synonyms.append(i["text"])
            self.optional_germ_synonyms = germ_synonyms
