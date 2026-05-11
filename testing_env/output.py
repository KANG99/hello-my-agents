import streamlit as st
import requests
import os
import time
import json

# 设置页面标题
st.set_page_config(page_title="Au(T+D)价格监控", layout="centered")

# 页面标题
st.title("💰 Au(T+D)黄金价格监控")

# 从环境变量获取API Key
api_key = os.getenv('GOLD_API_KEY', '')

# 如果没有设置API Key，显示警告信息
if not api_key or len(api_key) < 8:
    st.error("⚠️ 环境变量 GOLD_API_KEY 未正确配置或格式无效")
    st.stop()

# API配置
api_url = 'https://web.juhe.cn/finance/gold/shgold'  # 使用HTTPS

# 初始化 session state
if 'last_fetch_time' not in st.session_state:
    st.session_state['last_fetch_time'] = time.time()

# 初始化成功数据缓存
if 'last_successful_data' not in st.session_state:
    st.session_state['last_successful_data'] = None

# 缓存数据，避免频繁请求API
@st.cache_data(ttl=60)  # 缓存1分钟
def fetch_gold_data(refresh_key):
    """获取黄金数据"""
    try:
        params = {
            'key': api_key,
            'v': '1'
        }
        
        response = requests.get(api_url, params=params, timeout=10)
        response.raise_for_status()  # 自动抛出 4xx/5xx HTTPError
        
        data = response.json()
        
        if data.get('resultcode') == '200':
            return data.get('result', [{}])[0]  # 返回第一个结果
        else:
            return None
            
    except requests.exceptions.Timeout:
        return None
    except requests.exceptions.HTTPError:
        return None
    except json.JSONDecodeError:
        return None
    except requests.exceptions.RequestException:
        return None
    except Exception:
        return None

def clean_value(value):
    """清洗数据值，处理NaN和--"""
    if value is None or str(value).strip() in ('', 'NaN', '--', 'null', 'None'):
        return None
    return str(value)

def format_price(price):
    """格式化价格显示"""
    if price is None:
        return "N/A"
    try:
        return f"{float(price):.2f}"
    except (ValueError, TypeError):
        return "N/A"

def calculate_change(current_price, yesterday_price):
    """计算涨跌额和涨跌幅"""
    if current_price is None or yesterday_price is None:
        return "N/A", "N/A"
    
    try:
        current = float(current_price)
        yesterday = float(yesterday_price)
        change_amount = current - yesterday
        change_percent = (change_amount / yesterday) * 100 if yesterday != 0 else 0
        
        return f"{change_amount:.2f}", f"{change_percent:.2f}%"
    except (ValueError, TypeError):
        return "N/A", "N/A"

# 获取数据
with st.spinner("⏳ 正在同步黄金交易所数据..."):
    gold_data = fetch_gold_data(st.session_state['last_fetch_time'])

# 如果获取失败，尝试使用缓存数据
if gold_data is None:
    gold_data = st.session_state.get('last_successful_data')
    if gold_data is None:
        st.error("❌ 无法获取数据，请检查API配置或网络连接")
        st.stop()
    else:
        st.warning("⚠️ 实时接口异常，已降级显示缓存数据")

# 如果获取成功，更新缓存
if gold_data is not None:
    st.session_state['last_successful_data'] = gold_data

# 显示数据
if gold_data:
    # 获取Au(T+D)数据
    au_t_d_data = gold_data.get('Au(T+D)', {})
    
    if not au_t_d_data:
        st.warning("⚠️ 未获取到Au(T+D)数据")
    else:
        # 提取关键字段
        latest_price = clean_value(au_t_d_data.get('latestpri'))
        open_price = clean_value(au_t_d_data.get('openpri'))
        yesterday_price = clean_value(au_t_d_data.get('yespri'))
        max_price = clean_value(au_t_d_data.get('maxpri'))
        min_price = clean_value(au_t_d_data.get('minpri'))
        
        # 计算涨跌额和涨跌幅
        change_amount, change_percent = calculate_change(latest_price, yesterday_price)
        
        # 显示当前价格
        delta_num = float(change_amount) if change_amount != "N/A" else 0
        st.metric(
            label="当前价格 (元/克)",
            value=format_price(latest_price),
            delta=delta_num
            # 移除 delta_color，避免API错误
        )
        
        # 显示涨跌幅
        if change_percent != "N/A":
            st.metric(
                label="涨跌幅",
                value=f"{change_percent}"
                # 移除 delta_color，避免API错误
            )
        else:
            st.metric(label="涨跌幅", value="N/A")
        
        # 显示其他信息
        col1, col2, col3 = st.columns(3)
        
        with col1:
            st.info(f"开盘价: {format_price(open_price)} 元/克")
        with col2:
            st.info(f"最高价: {format_price(max_price)} 元/克")
        with col3:
            st.info(f"最低价: {format_price(min_price)} 元/克")
        
        # 显示刷新按钮
        if st.button("🔄 刷新数据"):
            st.session_state['last_fetch_time'] = time.time()  # 更新时间戳
            st.rerun()  # 重新运行应用
            
        # 显示数据更新时间
        st.caption(f"数据更新时间: {au_t_d_data.get('time', '未知')}")
        
else:
    st.error("❌ 无法获取数据，请检查API配置或网络连接")

# 添加说明信息
st.sidebar.header("📊 使用说明")
st.sidebar.markdown("""
- 本应用显示上海黄金交易所Au(T+D)实时价格
- 数据每分钟更新一次
- 点击"刷新数据"按钮可手动更新
- 如遇网络问题，请稍后重试
""")

st.sidebar.header("🔑 API配置")
st.sidebar.markdown("""
1. 请在环境变量中设置 `GOLD_API_KEY`
2. 该API需要有效的key才能获取数据
3. 如无key，请联系API提供商
""")