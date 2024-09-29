import sys
import glob

assets_dir = "assistant/static/assets/"


def main(api_url):
    for filename in glob.glob(assets_dir+"/index-*.css"):
        with open(filename) as f:
            data = f.read()
            data = data.replace("192.168.0.11:8000", api_url)
            with open(assets_dir+"index.css", "w") as w:
                w.write(data)

    for filename in glob.glob(assets_dir+"/index-*.js"):
        with open(filename) as f:
            data = f.read()
            data = data.replace("192.168.0.11:8000", api_url)
            with open(assets_dir+"index.js", "w") as w:
                w.write(data)


if __name__ == "__main__":
    argv = sys.argv
    print(argv)
    main(argv[1])
