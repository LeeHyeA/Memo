from tkinter import *   # 윈도우 프로그래밍
import os                   # 파일 이름
from tkinter.filedialog import *        # 파일선택창
from tkinter.simpledialog import *      # 대화상자
from tkinter import messagebox      # 메세지 박스

dragSelect = ""
imgList = []

def _newFile():
    window.title("제목없음- 메모장")
    file = None 
    text.delete(1.0,END)    # 메모장 text 초기화

def _openFile():
    file = askopenfilename(title = "파일 선택"
                           , filetypes = (("텍스트 파일", "*.txt"),("모든 파일", "*.*")))     # 불러올 파일 선택창 띄우기
    window.title(os.path.basename(file) + " - 메모장")         # basename() : 파일의 기본이름 반환
    text.delete(1.0, END)
    f = open(file,"r")          # 파일 불러오기
    text.insert(1.0,f.read())
    f.close()

def _saveFile():
    f = asksaveasfile(mode = "w", defaultextension=".txt")      # 저장할 파일 선택창 띄우기
    if f is None:
        return
    ts = str(text.get(1.0, END))
    f.write(ts)
    f.close()

def _image() :
    loadFile = askopenfilename(title = "파일 선택"
                       , filetypes = (("PNG 파일", "*.png"),("GIF 파일", "*.gif"),("모든 파일", "*.*")))     # 불러올 파일 선택창 띄우기
    print(loadFile)

    fname, ext = os.path.splitext(loadFile) # 경로에서 확장자 분리
    if ext == ".JPG" :      # JPG는 PhotoImage() 지원을 안하는거 같음.
        loadFile = fname + ".jpg"

    img = PhotoImage(file = loadFile)
    imgList.append(img)
    text.image_create(END, image = imgList[-1])
    
    '''
    #text.image_create(END, image = imgList[-1])    # 하얀색으로보임
    text.window_create(END, window = Label(text, image = imgList[-1]))  # 회색으로보임
    Button(window, image = imgList[-1]).pack()
    '''
    
def _cut():
    global dragSelect
    dragSelect = text.get(SEL_FIRST, SEL_LAST)
    if dragSelect == "" :       # 드래그한 부분이 없을때 예외처리
        return
    text.delete(SEL_FIRST, SEL_LAST)    # 드래그한 부분 삭제

def _copy():
    global dragSelect
    dragSelect = text.get(SEL_FIRST, SEL_LAST)      # 드래그한 부분 dragSelect 저장

def _paste():
    global dragSelect
    if dragSelect == "" :       # 드래그한 부분이 없을때 예외처리
        return
    text.insert(INSERT, dragSelect)         # 커서 위치에 붙여넣기

def _delete():
    text.delete(SEL_FIRST, SEL_LAST)    # 드래그한 부분 삭제

def _help():
    he = Toplevel(window)
    he.geometry("200x200")
    he.title("정보")
    lb = Label(he, text = "메모장 1.0\n B577031 이현경")
    lb.pack()

def _find() :
    findStr = askstring("문자 찾기", "찾으려고 하는 문자를 입력하세요.")
    textStr = text.get(1.0, END);
    if textStr.count(findStr) == 0 :
        messagebox.showinfo("검색 실패", "찾으려는 문자가 없습니다.")
    else :
        messagebox.showinfo("검색 결과", str(textStr.count(findStr))+"개의 문자가 있습니다.")

def _move() :
    findLine = askstring("열 이동", "이동하려는 열을 입력하세요.")
    text.tag_add("move", findLine+".0", findLine+".end")
    text.tag_config("move", background="skyblue", foreground="black")

def _special() :
    text.tag_add("special", SEL_FIRST, SEL_LAST)
    text.tag_config("special", background="yellow", foreground="red")

def _nomal() :
    text.tag_remove("special", 1.0, END)

def _font() :
    fontName = askstring("글꼴", "변경할 글꼴 이름을 입력하세요.")
    fontSize = askinteger("크기", "변경할 글씨 크기를 입력하세요.", minvalue = 10, maxvalue = 100)
    text.configure(font=(fontName, fontSize))

                        
window = Tk()
window.title("메모장")
window.geometry("600x600")

text = Text(window, undo=True)          # 실행취소 기능 사용
scrollBar = Scrollbar(text)                    # text에 스크롤바 붙이기
scrollBar.config(command = text.yview)                 # text와 scroll 연결
window.grid_rowconfigure(0, weight=1)           # 가로를 전체 크기로
window.grid_columnconfigure(0, weight=1)    # 세로를 전체 크기로
scrollBar.pack(side = RIGHT, fill = Y)                                      # scroll을 text 오른쪽에 위치
text.grid(sticky = N + E + S + W)
file = None


menuBar = Menu(window)
fileMenu = Menu(menuBar, tearoff = 0)       # tearoff(첫 절취선)를 표시하지 않음
menuBar.add_cascade(label = "파일", menu = fileMenu) # 파일 메뉴를 메뉴바에 붙이기

fileMenu.add_command(label = "새 파일", command = _newFile)
fileMenu.add_command(label = "열기", command = _openFile)
fileMenu.add_command(label = "저장", command = _saveFile)
fileMenu.add_command(label = "이미지", command = _image)
fileMenu.add_separator()      # 구분선
fileMenu.add_command(label = "종료", command = window.destroy)


rewriteMenu = Menu(menuBar, tearoff = 0)    # tearoff(첫 절취선)를 표시하지 않음
menuBar.add_cascade(label = "편집", menu = rewriteMenu)      # 편집 메뉴를 메뉴바에 붙이기

rewriteMenu.add_command(label = "찾기", command = _find)
rewriteMenu.add_separator()      # 구분선
rewriteMenu.add_command(label = "잘라내기", command = _cut)
rewriteMenu.add_command(label = "복사", command = _copy)
rewriteMenu.add_command(label = "붙여넣기", command = _paste)
rewriteMenu.add_command(label = "삭제", command = _delete)
rewriteMenu.add_separator()      # 구분선
rewriteMenu.add_command(label = "이동", command = _move)
rewriteMenu.add_command(label = "형광펜", command = _special)
rewriteMenu.add_command(label = "형광펜 제거", command = _nomal)


formMenu = Menu(menuBar, tearoff = 0) # tearoff(첫 절취선)를 표시하지 않음
menuBar.add_cascade(label = "서식", menu=formMenu)  # 서식을 메뉴바에 붙이기
formMenu.add_command(label = "글꼴", command = _font)


helpMenu = Menu(menuBar, tearoff = 0) # tearoff(첫 절취선)를 표시하지 않음
menuBar.add_cascade(label = "도움말", menu=helpMenu)  # 도움말을 메뉴바에 붙이기
helpMenu.add_command(label = "메모장 정보", command = _help)


window.config(menu=menuBar)     # 메뉴바를 연결
window.bind("<Escape>",  lambda x: window.destroy())    # esc 키를 눌렀을때 종료
window.bind("<Control-v>", lambda x: _paste())
window.bind("<Control-f>", lambda x: _find())
window.bind("<Key>", lambda x:  text.tag_remove("move", 1.0, END)) # 줄찾기 지움

for i in imgList :
    Button(window, image = imgList[i]).pack()   # 그림 출력


window.mainloop()



