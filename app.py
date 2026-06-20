from __future__ import annotations

from datetime import date
from io import BytesIO
from typing import Any

import qrcode
import streamlit as st


st.set_page_config(
    page_title="PawHandoff AI",
    page_icon="🐾",
    layout="wide",
    initial_sidebar_state="expanded",
)


st.markdown(
    """
    <style>
    .stApp { background: #fbfaf7; }
    .hero {
        padding: 1.7rem 2rem; border-radius: 22px;
        background: linear-gradient(120deg, #173f35, #2c6a58);
        color: white; margin-bottom: 1.2rem;
    }
    .hero h1 { margin: 0; font-size: 2.25rem; }
    .hero p { margin: .55rem 0 0; color: #e4f3eb; max-width: 760px; }
    .soft-card {
        background: white; border: 1px solid #e9e4da; border-radius: 16px;
        padding: 1rem 1.15rem; margin: .5rem 0 1rem;
    }
    .eyebrow { color: #c96d42; font-weight: 700; letter-spacing: .06em; }
    div[data-testid="stMetric"] { background: white; border: 1px solid #e9e4da; padding: 12px; border-radius: 14px; }
    .stButton > button, .stDownloadButton > button { border-radius: 10px; }
    </style>
    """,
    unsafe_allow_html=True,
)


def value(data: dict[str, Any], key: str, fallback: str = "未特别说明") -> str:
    raw = data.get(key)
    return str(raw).strip() if raw not in (None, "", []) else fallback


def ai_generate_handoff_pack(inputs: dict[str, Any]) -> str:
    """Mock AI：后续可在此替换为 OpenAI API 或其他大模型 API。"""
    name = value(inputs, "pet_name", "宠物")
    pet_type = value(inputs, "pet_type")
    toilet_label = "猫砂管理" if pet_type == "猫" else "遛狗/排泄" if pet_type == "狗" else "清洁与排泄"
    medication = value(inputs, "medication", "不需要")
    return f"""# {name}的照顾交接包

> 场景：{value(inputs, 'care_scene')}｜周期：{inputs.get('care_days', 1)} 天｜生成日期：{date.today().isoformat()}

## 1. 宠物照顾说明书

- **基本信息**：{name}，{pet_type}，{value(inputs, 'age')}；性格/互动特点：{value(inputs, 'personality')}。
- **喂食**：{value(inputs, 'feeding_time')}；食物与用量：{value(inputs, 'food')}。
- **饮水**：{value(inputs, 'water')}。
- **{toilet_label}**：{value(inputs, 'toilet_walk')}。
- **用药**：{medication}。
- **禁忌事项**：{value(inputs, 'taboos')}。
- **空间边界**：允许进入 {value(inputs, 'allowed_areas')}；禁止进入 {value(inputs, 'forbidden_areas')}。
- **紧急联系人**：{value(inputs, 'emergency_contact')}。
- **主人补充**：{value(inputs, 'notes')}。

## 2. 每日照顾任务清单

- [ ] 按 {value(inputs, 'feeding_time')} 喂食，并确认进食情况
- [ ] 按要求换水、检查饮水情况
- [ ] 完成{toilet_label}，观察排泄是否异常
- [ ] 观察精神、呼吸、行动与互动状态
- [ ] 如需用药，按交代执行并记录
- [ ] 拍摄食盆、水碗及{toilet_label}照片
- [ ] 记录异常或与平日不同的表现
- [ ] 离开前确认门窗、门锁及环境安全

## 3. 异常情况处理流程

**观察并记录 → 暂停自行增加食物/药物等处理 → 联系主人 → 按主人或专业兽医建议行动。**

重点判断：{value(inputs, 'abnormal_signs')}。若出现持续不吃不喝、反复呕吐/腹泻、无法排尿、呼吸异常、意识或行动明显异常等情况，应立即联系主人；联系不上时联系备用联系人，并视紧急程度咨询附近正规宠物医院。此工具只辅助交接与留痕，不替代兽医判断。

## 4. 给照护方的简洁版说明

请按时为{name}完成喂食、换水和{toilet_label}，重点留意精神、进食与排泄。仅进入允许区域，不进入禁入区域；发现异常先拍照记录并联系主人，不自行改变喂养或用药方案。离开前请再次确认门窗和门锁。

## 5. 主人出门前准备清单

- [ ] 按天分装并标注食物/药物
- [ ] 准备充足饮水、清洁用品与垃圾袋
- [ ] 明确钥匙交接、允许及禁入区域
- [ ] 留下紧急联系人、宠物医院和备用方案
- [ ] 与照护方共同确认本交接包，必要时现场演示

## 6. 隐私与安全提醒

照片只记录任务结果与宠物状态，避免拍摄私人文件、屏幕或无关生活区域；仅进入主人授权区域，不进行无关翻动。离开前确认宠物处于安全区域，门窗、燃气/电器（如涉及）和门锁状态正常。照片及记录仅用于本次照护沟通，双方约定保存期限后及时删除。
"""


def ai_generate_daily_report(checkin_data: dict[str, Any]) -> str:
    """Mock AI：保持统一接口，未来可把函数体替换为真实模型调用。"""
    pet_name = checkin_data.get("pet_name", "宠物")
    tasks: dict[str, bool] = checkin_data.get("tasks", {})
    done = [label for label, checked in tasks.items() if checked]
    undone = [label for label, checked in tasks.items() if not checked]
    notes = value(checkin_data, "notes", "未填写异常备注")
    abnormal = checkin_data.get("has_abnormal", False) or bool(checkin_data.get("notes", "").strip())
    photos = checkin_data.get("photo_count", 0)
    done_text = "、".join(done) if done else "暂无已勾选任务"
    undone_text = "、".join(undone) if undone else "无"
    food = "已完成喂食记录" if tasks.get("已喂食") else "未确认喂食"
    water = "已完成换水记录" if tasks.get("已换水") else "未确认换水"
    toilet = "已完成排泄相关任务" if tasks.get("已铲猫砂 / 已遛狗") else "未确认排泄相关任务"
    state = "已观察，未备注明显异常" if tasks.get("已观察宠物精神状态") and not abnormal else "需要主人关注备注内容" if abnormal else "尚未确认"
    status = "有待确认事项" if abnormal or undone else "本次未记录明显异常"
    tomorrow = "继续按原计划照护，并对照交接包观察进食、饮水、排泄与精神状态。"
    if abnormal:
        tomorrow = "优先复查本次备注涉及的状态，及时给主人同步；不要自行改变饮食或用药方案。"
    wechat = (
        f"{pet_name}今日照护已打卡：{done_text}。状态：{state}。"
        f"照片共{photos}张；备注：{notes}。明日将继续按交接要求照护，有变化会及时同步。"
    )
    return f"""# {pet_name}的今日照顾报告

> 日期：{date.today().isoformat()}｜本报告由打卡信息自动整理，仅用于照护沟通。

## 1. 今日任务完成情况

- **已完成**：{done_text}
- **待确认/未勾选**：{undone_text}

## 2. 宠物状态摘要

{state}。照护方备注：{notes}。

## 3. 饮食、饮水、排泄情况

- 饮食：{food}
- 饮水：{water}
- 排泄：{toilet}

## 4. 是否有异常

**{status}**。如状态持续或加重，请主人和照护方及时沟通，并在需要时咨询专业兽医。

## 5. 照片证据说明

本次上传 {photos} 张照片，用于辅助说明任务结果与宠物状态；照片本身不能替代现场判断。

## 6. 明天需要注意什么

{tomorrow}

## 7. 微信简洁汇报

{wechat}
"""


def make_qr(payload: str) -> bytes:
    qr = qrcode.QRCode(version=2, box_size=8, border=3)
    qr.add_data(payload)
    qr.make(fit=True)
    image = qr.make_image(fill_color="#173f35", back_color="white")
    output = BytesIO()
    image.save(output, format="PNG")
    return output.getvalue()


for key, default in {"handoff_pack": "", "daily_report": "", "pet_profile": {}, "last_checkin": {}}.items():
    if key not in st.session_state:
        st.session_state[key] = default


with st.sidebar:
    st.markdown("### 🐾 PawHandoff AI")
    st.caption("宠物代喂与寄养智能交接助手")
    st.markdown(
        """
        **演示流程**

        1. 主人填写信息并生成交接包
        2. 照护方按任务打卡并留痕
        3. AI 自动整理给主人看的日报
        4. 二维码照护卡快速进入任务
        """
    )
    st.info("MVP 不提供人员派单、定位监控或安全担保；目标是标准化流程，降低双方沟通成本与误解。")


st.markdown(
    """
    <section class="hero">
      <div class="eyebrow">PAWHANDOFF AI · MVP</div>
      <h1>每次托付，都交代得更清楚</h1>
      <p>把零散的宠物习惯整理成交接说明与每日任务，再将照护方的打卡自动汇总成一份可信、克制、易沟通的今日报告。</p>
    </section>
    """,
    unsafe_allow_html=True,
)

tab_owner, tab_checkin, tab_report, tab_qr = st.tabs(
    ["🏠 主人端生成交接包", "✅ 代喂人 / 寄养方打卡", "📋 今日报告", "▦ 二维码照护卡"]
)


with tab_owner:
    st.subheader("创建宠物照顾交接包")
    st.caption("带 * 的内容建议尽量具体；生成后仍应由主人和照护方共同确认。")
    with st.form("owner_form"):
        c1, c2, c3 = st.columns(3)
        pet_name = c1.text_input("宠物名字 *", placeholder="例如：奶盖")
        pet_type = c2.selectbox("宠物类型 *", ["猫", "狗", "其他"])
        age = c3.text_input("年龄", placeholder="例如：3岁")

        personality = st.multiselect(
            "性格与互动特点",
            ["胆小", "亲人", "怕生", "容易应激", "会回应名字", "护食", "不喜欢被抱", "精力旺盛"],
        )
        p_extra = st.text_input("其他性格说明", placeholder="例如：听到吸尘器会躲到床下")
        c1, c2 = st.columns(2)
        care_scene = c1.selectbox("照顾场景 *", ["上门代喂", "寄养", "朋友临时代看"])
        care_days = c2.number_input("照顾天数 *", min_value=1, max_value=60, value=3)

        st.markdown("#### 日常照护")
        c1, c2 = st.columns(2)
        feeding_time = c1.text_input("喂食时间 *", placeholder="例如：每天 08:00、19:00")
        food = c2.text_input("食物类型和用量 *", placeholder="例如：猫粮每次 35g，湿粮晚间半罐")
        water = c1.text_area("饮水要求", placeholder="例如：每天换水并清洗水碗", height=100)
        toilet_walk = c2.text_area("猫砂 / 遛狗要求", placeholder="例如：早晚各铲一次；或每天遛狗两次", height=100)
        medication = st.text_area("是否需要喂药", placeholder="若需要，请写药名、剂量、时间、方法和注意事项；否则填“不需要”")

        st.markdown("#### 安全边界与异常")
        taboos = st.text_area("禁忌事项", placeholder="例如：不能吃人类食物，不要强行抱起")
        c1, c2 = st.columns(2)
        allowed_areas = c1.text_input("允许进入区域", placeholder="例如：玄关、客厅、厨房")
        forbidden_areas = c2.text_input("禁入区域", placeholder="例如：主卧、书房")
        abnormal_signs = st.text_area(
            "异常情况判断",
            value="连续不吃饭、反复呕吐或腹泻、不排尿、精神明显变差、呼吸或行动异常",
        )
        emergency_contact = st.text_input("紧急联系人 *", placeholder="例如：主人 138****0000 / 备用联系人及宠物医院")
        notes = st.text_area("主人补充说明", placeholder="其他熟悉宠物的小技巧、物品位置或交接约定")

        submitted = st.form_submit_button("✨ 生成交接包", type="primary", use_container_width=True)

    if submitted:
        if not pet_name or not feeding_time or not food or not emergency_contact:
            st.error("请先填写宠物名字、喂食时间、食物用量和紧急联系人。")
        else:
            profile = {
                "pet_name": pet_name,
                "pet_type": pet_type,
                "age": age,
                "personality": "、".join(personality + ([p_extra] if p_extra else [])),
                "care_scene": care_scene,
                "care_days": care_days,
                "feeding_time": feeding_time,
                "food": food,
                "water": water,
                "toilet_walk": toilet_walk,
                "medication": medication,
                "taboos": taboos,
                "allowed_areas": allowed_areas,
                "forbidden_areas": forbidden_areas,
                "abnormal_signs": abnormal_signs,
                "emergency_contact": emergency_contact,
                "notes": notes,
            }
            st.session_state.pet_profile = profile
            st.session_state.handoff_pack = ai_generate_handoff_pack(profile)
            st.success("交接包已生成。请主人检查内容，并与照护方共同确认。")

    if st.session_state.handoff_pack:
        with st.expander("预览完整交接包", expanded=True):
            st.markdown(st.session_state.handoff_pack)
        st.download_button(
            "下载交接包 Markdown",
            st.session_state.handoff_pack,
            file_name=f"{st.session_state.pet_profile.get('pet_name', '宠物')}_照顾交接包.md",
            mime="text/markdown",
        )


with tab_checkin:
    profile = st.session_state.pet_profile
    if not profile:
        st.warning("请先在“主人端生成交接包”中创建一份交接包，再进行打卡。")
    else:
        st.subheader(f"{profile['pet_name']} · 今日照护任务")
        st.caption(f"{profile['care_scene']}｜第 1 / {profile['care_days']} 天（MVP 模拟）")
        task_labels = [
            "已喂食", "已换水", "已铲猫砂 / 已遛狗", "已观察宠物精神状态",
            "已拍摄食盆照片", "已拍摄水碗照片", "已拍摄猫砂盆 / 遛狗照片",
            "已确认门窗关闭", "已确认没有进入禁入区域",
        ]
        with st.form("checkin_form"):
            st.markdown("#### 勾选已完成任务")
            cols = st.columns(2)
            task_values = {
                label: cols[index % 2].checkbox(label, key=f"task_{index}")
                for index, label in enumerate(task_labels)
            }
            uploaded = st.file_uploader(
                "上传 1–3 张任务或宠物状态照片",
                type=["jpg", "jpeg", "png"],
                accept_multiple_files=True,
                help="Demo 仅在当前会话中使用文件，不写入数据库。",
            )
            has_abnormal = st.checkbox("发现需要主人关注的异常或不确定情况")
            checkin_notes = st.text_area("异常 / 补充备注", placeholder="如无异常可留空；请描述观察到的事实，避免自行诊断")
            checkin_submit = st.form_submit_button("提交今日打卡", type="primary", use_container_width=True)

        if checkin_submit:
            if len(uploaded) > 3:
                st.error("MVP 每次最多上传 3 张照片，请减少后再提交。")
            elif len(uploaded) == 0:
                st.error("请至少上传 1 张照片用于本次演示留痕。")
            else:
                checkin = {
                    "pet_name": profile["pet_name"], "tasks": task_values,
                    "has_abnormal": has_abnormal, "notes": checkin_notes,
                    "photo_count": len(uploaded), "photo_names": [f.name for f in uploaded],
                }
                st.session_state.last_checkin = checkin
                st.session_state.daily_report = ai_generate_daily_report(checkin)
                st.success("今日打卡已提交，AI 报告已整理。可切换到“今日报告”查看。")


with tab_report:
    if not st.session_state.daily_report:
        st.info("完成一次今日打卡后，这里会自动生成给主人看的照顾报告。")
    else:
        checkin = st.session_state.last_checkin
        done_count = sum(checkin["tasks"].values())
        c1, c2, c3 = st.columns(3)
        c1.metric("已完成任务", f"{done_count} / {len(checkin['tasks'])}")
        c2.metric("照片留痕", f"{checkin['photo_count']} 张")
        c3.metric("异常标记", "需关注" if checkin["has_abnormal"] or checkin["notes"] else "未标记")
        st.markdown(st.session_state.daily_report)
        st.download_button(
            "下载今日报告 Markdown",
            st.session_state.daily_report,
            file_name=f"{checkin['pet_name']}_{date.today().isoformat()}_今日照顾报告.md",
            mime="text/markdown",
        )


with tab_qr:
    profile = st.session_state.pet_profile
    pet_name = profile.get("pet_name", "奶盖（示例）")
    emergency = profile.get("emergency_contact", "主人 138****0000（示例）")
    payload = f"PawHandoff AI Demo | 宠物：{pet_name} | 查看今日照顾任务 | http://localhost:8501"
    st.subheader("二维码照护卡 · 概念展示")
    st.caption("MVP 二维码仅编码本地演示文本，不连接真实后端，也不包含完整隐私信息。")
    left, right = st.columns([1, 2])
    with left:
        st.image(make_qr(payload), width=240)
    with right:
        st.markdown(
            f"""
            <div class="soft-card">
              <div class="eyebrow">PAWHANDOFF CARE CARD</div>
              <h2>🐾 {pet_name}</h2>
              <h3>扫码查看今日照顾任务</h3>
              <p><b>紧急联系人：</b>{emergency}</p>
              <p style="color:#6b746f">仅供本次照护交接使用 · 请勿转发</p>
            </div>
            """,
            unsafe_allow_html=True,
        )
        st.code(payload, language=None)

st.divider()
st.caption("PawHandoff AI · 轻量机会验证 Demo｜流程标准化、任务打卡与照片留痕旨在降低沟通和信任风险，不构成安全担保或医疗建议。")
