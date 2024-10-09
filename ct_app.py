import streamlit as st
import time

def check_status():
    time.sleep(5)
    return st.session_state.status

def send_approved_mail():
    st.success('Email sent with attached CT registration file')

def send_rejected_mail():
    st.success('Email sent with reason of rejection')

def send_document_mail():
    st.success('Email sent for getting required documents')

def send_remind_mail():
    st.success('Email sent for reminding the client')

if 'status' not in st.session_state:
    st.session_state.status = ''
if 'stage' not in st.session_state:
    st.session_state.stage = ''

st.subheader("Please select the current stage and status of the application.")

st.session_state.stage = st.radio(
    'What is the Stage of CT registration?',
    options=['Filed', 'Resubmit'],
    horizontal=True
)
st.session_state.status = st.radio(
    'What is the Status of the Application?',
    options=['Approved', 'Rejected', 'More info needed'],
    horizontal=True
)

if st.session_state.stage == 'Filed':
    check_status_button = st.button('Check Status')
    if check_status_button:
        with st.spinner('Checking CT registration status'):
            status = check_status()
            if not status:
                st.stop()
            if status == 'Approved':
                st.success(status)
                send_approved_mail()
            elif status == 'Rejected':
                st.error(status)
                send_rejected_mail()
            else:
                st.warning(status)
                send_document_mail()
                st.session_state.stage = 'Resubmit'

elif st.session_state.stage == 'Resubmit':
    st.write('Has the customer replied?')
    col1, col2 = st.columns(2)
    customer_reply_yes = col1.button('Yes')
    customer_reply_no = col2.button('No')
    
    if customer_reply_yes:
        st.write('Time for resubmitting the CT file')
        
    if customer_reply_no:
        send_remind_mail()

if st.button('Reset'):
    st.session_state.status = ''
    st.session_state.stage = ''
    st.rerun()
