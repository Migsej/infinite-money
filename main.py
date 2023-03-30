import requests
import json
import ffmpeg
from api_key import API_KEY

VOICE_ID = "21m00Tcm4TlvDq8ikWAM"

def postname_comment(subreddit, posts):
    postarray = []
    print("getting post name")
    url = f"https://reddit.com/r/{subreddit}/top/.json?limit={posts}"
    postr = requests.get(url, headers={'Accept': 'application/json', 'User-agent': 'your bot 0.1'})
    #print(r.json())

    postjson = json.loads(postr.text)
    for i in range(posts):
        #print(title)
        
        title = postjson["data"]["children"][i]["data"]["title"]
        print("finding comment name")
        commenturl = postjson["data"]["children"][i]["data"]["url"]
        r = requests.get(f"{commenturl}.json?limit=1", headers={'Accept': 'application/json', "User-agent": "your bot 0.1"})
        jsonresponse = json.loads(r.text)
        comment = jsonresponse[1]["data"]["children"][0]["data"]["body"]
        #print(comment)
        postarray.append(f"{title} {comment}")


    return postarray 



def text_to_speech(text):
    print("getting audio")
    url = f"https://api.elevenlabs.io/v1/text-to-speech/{VOICE_ID}"
    jsonparam = {
      "text": text,
      "voice_settings": {
        "stability": 0,
        "similarity_boost": 0
      },
    }

    r = requests.post(url, headers = {'xi-api-key': API_KEY}, json = jsonparam)
    return r.content


def combine_video_audio(video, audio, outputname):
    return ffmpeg.concat(video, audio, v=1, a=1).output(outputname)



def main():
    posts = postname_comment("askreddit", 3)
    for i, name in enumerate(posts):
        with open("audio.mp3", "wb") as f:
            f.write(text_to_speech(name))
        input_audio = ffmpeg.input("./audio.mp3")

        audiolen = ffmpeg.probe("audio.mp3")['format']['duration']
        input_gameplay = ffmpeg.input("./gameplaynew.mp4") 
        listname = name.split(" ")
        print(audiolen)
        for j, text in enumerate(listname):
            wordlen = float(audiolen) / len(listname)

            input_gameplay = input_gameplay.drawtext(text=text,
                fontfile="./static/SourceCodePro-Medium.ttf",
                fontcolor="white",x="(w-tw)/2",y="((h-text_h)/2)-(text_h-(th/4))",
                fontsize="64",enable=f"between(t,{j*wordlen},{(j+1)*wordlen})")

        combined = combine_video_audio(input_gameplay.trim(start=0, end=audiolen), input_audio, f"./finished{i}.mp4")
        
        combined.run()

if __name__ == "__main__":
    main()
