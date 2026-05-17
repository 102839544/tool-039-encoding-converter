#!/usr/bin/env python3
"""
文件编码转换工具 - 批量转换文件编码
"""
import sys, os, tkinter as tk
from pathlib import Path
from tkinter import filedialog, messagebox
import tkinter as tk

class App:
    def __init__(self, root):
        self.root = root
        root.title("文件编码转换工具 v1.0")
        root.geometry("650x550")
        self.files = []
        self.build_ui()
    
    def build_ui(self):
        f = tk.Frame(self.root, bg="#455a64", height=50)
        f.pack(fill="x")
        tk.Label(f, text="📝 文件编码转换工具", font=("Arial",14,"bold"),
                 fg="white", bg="#455a64").pack(pady=12)
        
        main = tk.Frame(self.root, padx=15, pady=10)
        main.pack(fill="both", expand=True)
        
        bf = tk.Frame(main)
        bf.pack(fill="x", pady=5)
        tk.Button(bf, text="添加文件", command=self.add_files,
                  bg="#455a64", fg="white", padx=12).pack(side="left", padx=5)
        tk.Button(bf, text="清空列表", command=self.clear,
                  bg="#d9534f", fg="white", padx=12).pack(side="left", padx=5)
        
        self.lb = tk.Listbox(main, font=("Consolas",10), bg="#eceff1", height=10)
        self.lb.pack(fill="both", expand=True, pady=10)
        
        # 编码选择
        ef = tk.Frame(main)
        ef.pack(fill="x", pady=10)
        tk.Label(ef, text="源编码：").pack(side="left")
        self.src_enc = tk.StringVar(value="auto")
        encodings = ["auto", "utf-8", "utf-8-sig", "gbk", "gb2312", "big5", "shift-jis", "iso-8859-1"]
        self.src_combo = tk.Combobox(ef, textvariable=self.src_enc,
                                      values=encodings, state="readonly", width=12)
        self.src_combo.pack(side="left", padx=10)
        
        tk.Label(ef, text="目标编码：").pack(side="left", padx=(20,0))
        self.dst_enc = tk.StringVar(value="utf-8")
        self.dst_combo = tk.Combobox(ef, textvariable=self.dst_enc,
                                      values=["utf-8", "utf-8-sig", "gbk", "gb2312", "big5"],
                                      state="readonly", width=12)
        self.dst_combo.pack(side="left", padx=10)
        
        tk.Button(ef, text="开始转换", command=self.convert,
                  bg="#4caf50", fg="white", font=("Arial",10,"bold"),
                  padx=20).pack(side="right", padx=10)
        
        self.status = tk.Label(main, text="添加文本文件后选择编码进行转换",
                               font=("Arial",10), fg="gray")
        self.status.pack()
    
    def add_files(self):
        fs = filedialog.askopenfilenames(title="选择文件",
             filetypes=[("文本文件","*.txt *.csv *.json *.xml *.py *.js *.html *.css *.md")])
        for f in fs:
            if f not in self.files:
                self.files.append(f)
                self.lb.insert("end", Path(f).name)
        self.status.config(text=f"已添加 {len(self.files)} 个文件")
    
    def clear(self):
        self.files.clear()
        self.lb.delete(0, "end")
        self.status.config(text="列表已清空")
    
    def detect_encoding(self, file_path):
        """简单编码检测"""
        try:
            import chardet
            with open(file_path, "rb") as f:
                raw = f.read(10000)
                result = chardet.detect(raw)
                return result.get("encoding", "utf-8")
        except:
            return "utf-8"
    
    def convert(self):
        if not self.files:
            messagebox.showwarning("提示", "请先添加文件")
            return
        
        src = self.src_enc.get()
        dst = self.dst_enc.get()
        ok = 0
        
        for f in self.files:
            try:
                # 检测编码
                if src == "auto":
                    enc = self.detect_encoding(f)
                else:
                    enc = src
                
                # 读取并转换
                with open(f, "r", encoding=enc, errors="ignore") as file:
                    content = file.read()
                
                with open(f, "w", encoding=dst) as file:
                    file.write(content)
                
                ok += 1
            except Exception as e:
                print(f"转换失败 {f}: {e}")
        
        messagebox.showinfo("完成", f"成功转换 {ok}/{len(self.files)} 个文件")
        self.status.config(text=f"✅ 完成：{ok}/{len(self.files)} 个文件")

if __name__ == "__main__":
    root = tk.Tk()
    App(root)
    root.mainloop()
