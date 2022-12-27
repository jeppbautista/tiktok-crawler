class Root:
    CONTAINERS = """//*[@id="app"]/div[2]/div[2]/div[1]/div"""

class ContainerItem(Root):
    UNIQUEID = ".//div[1]/div[1]/div[1]/a[2]/h3"
    AVATAR = ".//div[1]/div[1]/div[1]/a[1]/div[1]/span[1]/img"
    LINK = ".//a[1]"
    NICKNAME = ".//div[1]/div[1]/div[1]/a[2]/h4"
