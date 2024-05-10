import flet as ft;

#? def means defines, It's used to define new functions
def main(page):
  
  title = ft.Text("Hashzap")
  chat = ft.Column()
  username = ft.TextField(label="Your Name")

  def sendMessageToChannel(message):
    #? gets message type to differ from users joining chat from actual messages
    type = message["type"]
    if type == "message":
      user_message = message["user"]
      text_message = message["text"]
      #? adds message to chat column
      chat.controls.append(ft.Text(f"{user_message}: {text_message}"))
    else:
      user_message = message["user"]
      chat.controls.append(
        ft.Text(f"{user_message} entrou no chat", size=12, italic=True, color=ft.colors.ORANGE_500)
      )
      page.update()

  #? creates pubsub channel
  page.pubsub.subscribe(sendMessageToChannel)

  def sendMessage(event):
    page.pubsub.send_all({"text": messageInput.value, "user": username.value, "type": "message"})
    #? clears message input
    messageInput.value = ""
    page.update()

  #? onsubmit sends message on enter
  messageInput = ft.TextField(label="Type your message", on_submit=sendMessage)
  sendMessageButton = ft.ElevatedButton("Send", on_click=sendMessage)

  def joinChat(event):
    #? sends "user joined chat" notification and adds chat element to page
    page.pubsub.send_all({"user": username.value, "type": "entrada"})
    page.add(chat)
    
    #? closes popup and for "immersion" removes elements from page
    popup.open = False
    page.remove(showPopUpButton)
    page.remove(title)
    
    #? adds both elements for sending messages at the same time
    page.add(ft.Row([messageInput, sendMessageButton]))
    page.update()

  popup = ft.AlertDialog(
    open=False, 
    modal=True,
    title=ft.Text("Welcome to Hashzap"),
    content=username,
    actions=[ft.ElevatedButton("Join chat", on_click=joinChat)],
  )

  def showPopUp(event):
    page.dialog = popup
    popup.open = True
    page.update()

  showPopUpButton = ft.ElevatedButton("Iniciar chat", on_click=showPopUp)

  page.add(title)
  page.add(showPopUpButton)

ft.app(target=main, view=ft.WEB_BROWSER, port=8000)

ft.app(main, view=ft.WEB_BROWSER)
