from .global_variables import *
from .link_helpers import *

def get_opener():

    return f"""
        <!DOCTYPE html>
        <html lang="en-US">
            <head>
                <meta name="viewport" content="width=device-width, initial-scale=1, minimum-scale=1" />
                <link rel="preconnect" href="https://fonts.googleapis.com">
                <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
                <link href="https://fonts.googleapis.com/css2?family=Ubuntu:ital,wght@0,300;0,400;0,500;0,700;1,300;1,400;1,500;1,700&display=swap" rel="stylesheet">
                <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/4.7.0/css/font-awesome.min.css">
                <link rel="apple-touch-icon" sizes="180x180" href="/apple-touch-icon.png">
                <link rel="icon" type="image/png" sizes="32x32" href="/favicon-32x32.png">
                <link rel="icon" type="image/png" sizes="16x16" href="/favicon-16x16.png">
                <link rel="manifest" href="/site.webmanifest">
                <link rel="stylesheet" href="{directory_path}/style.css">
                <script type="text/javascript" src="{directory_path}/random.js"></script>
                {custom_header_html}
        """

def get_header():
    return f"""
        </head>
        <body onLoad=\"random()\">
            <div id=\"head\">
                <div class=\"keywords border\">
                    <a href=\"{format_link(f'{directory_path}/index.html')}\">
                        <p>Home</p>
                    </a>
                </div>
                <div class=\"keywords border\">
                    <a href=\"{format_link(f'{directory_path}/about.html')}\">
                        <p>About</p>
                    </a>
                </div>
                <div class=\"keywords border\">
                    <a href=\"{format_link(f'{directory_path}/search.html')}\">
                        <p>Search</p>
                    </a>
                </div>
                <div class=\"keywords random border\">
                    <a>
                        <p>Random</p>
                    </a>
                </div>
                <a href=\"https://www.instagram.com/cookingwithspud/\" target=\"_blank\" style=\"margin-left: auto; margin-right: 0.8rem; align-self: center; font-size: 1.8rem; color: inherit;\">
                    <i class=\"fa fa-instagram\"></i>
                </a>
            </div>
        <div id=\"body\">"""