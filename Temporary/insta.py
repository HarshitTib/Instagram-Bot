from instagrapi import Client

username = "suwichar2023"
password = "Suwichar@2023"

cl = Client()
cl.login(username, password)

media = cl.photo_upload(
    path = "./TemplatesImage/Output/Charles R_ Swindoll1.jpg",
    caption = "Quote 1"
)