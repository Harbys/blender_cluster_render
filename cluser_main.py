import threading
import web_dashboard

# s, e, t = blend_render_info.get_frames_info('/Users/harbys/Desktop/blenders/pr_susan/pr_susan.blend')
# print(f"s:{s}, e:{e}, t:{t}")


bt2 = threading.Thread(target=web_dashboard.run)
bt2.start()
