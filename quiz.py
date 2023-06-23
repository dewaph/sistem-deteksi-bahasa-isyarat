import streamlit as st
import random
from PIL import Image

def get_randomized_images():
    alphabet_images = {
        'A': 'quiz/A.png',
        'B': 'quiz/B.png',
        'C': 'quiz/C.png',
        'D': 'quiz/D.png',
        'E': 'quiz/E.png',
        'F': 'quiz/F.png',
        'G': 'quiz/G.png',
        'H': 'quiz/H.png',
        'I': 'quiz/I.png',
        'J': 'quiz/J.png',
        'K': 'quiz/K.png',
        'L': 'quiz/L.png',
        'M': 'quiz/M.png',
        'N': 'quiz/N.png',
        'O': 'quiz/O.png',
        'P': 'quiz/P.png',
        'Q': 'quiz/Q.png',
        'R': 'quiz/R.png',
        'S': 'quiz/S.png',
        'T': 'quiz/T.png',
        'U': 'quiz/U.png',
        'V': 'quiz/V.png',
        'W': 'quiz/W.png',
        'X': 'quiz/X.png',
        'Y': 'quiz/Y.png',
        'Z': 'quiz/Z.png'
        # Tambahkan path ke gambar huruf abjad lainnya sesuai dengan pilihan Anda
    }

    randomized_alphabet = random.sample(list(alphabet_images.keys()), len(alphabet_images))
    randomized_images = {letter: alphabet_images[letter] for letter in randomized_alphabet}

    return randomized_images

def get_randomized_options(options, correct_option):
    # Pastikan pilihan yang benar selalu ada di antara urutan 1-4 secara acak
    options.remove(correct_option)
    random.shuffle(options)
    random_index = random.randint(0, 3)
    randomized_options = options[:random_index] + [correct_option] + options[random_index:]
    return randomized_options

def app():
    st.title('QUIZ Huruf Alfabet BISINDO')

    question_prompts = [
        'Pilih jawaban yang sesuai dengan gambar dibawah:',
        # Tambahkan lebih banyak pertanyaan sesuai dengan jumlah pertanyaan yang Anda inginkan
    ]

    total_questions = 1

    if 'randomized_images' not in st.session_state:
        st.session_state.randomized_images = get_randomized_images()

    if 'randomized_options' not in st.session_state:
        st.session_state.randomized_options = None

    user_answers = {}

    for i in range(total_questions):
        question = question_prompts[i]
        options = list(st.session_state.randomized_images.keys())
        correct_option = options[i]

        if i in user_answers:
            selected_option = user_answers[i]
        else:
            selected_option = None

        st.subheader(question)

        correct_image = st.session_state.randomized_images[correct_option]
        resized_image = Image.open(correct_image).resize((250, 250))
        st.image(resized_image, width=250)

        if st.session_state.randomized_options is None:
            st.session_state.randomized_options = get_randomized_options(options, correct_option)

        user_option_key = f'user_option_{i}'
        if selected_option is None:
            user_option = st.radio('', st.session_state.randomized_options[:4], key=user_option_key)
        else:
            user_option = st.radio('', st.session_state.randomized_options[:4], index=st.session_state.randomized_options.index(selected_option), key=user_option_key)

        user_answers[i] = user_option

    submit_button_key = f'submit_button'
    submit_button = st.button('Submit', key=submit_button_key)

    if submit_button:
        st.session_state.randomized_images = get_randomized_images()
        st.session_state.randomized_options = None

        next_button_clicked = st.button('Next', key='next_button', help='Klik tombol Next untuk melanjutkan')

        st.subheader('Hasil Akhir')
        for j in range(total_questions):
            user_option = user_answers[j]
            correct_option = options[j]

            if user_option == correct_option:
                st.balloons()
                st.write(f'Jawaban Anda benar')

            else:
                st.markdown('<p style="color: red;">Jawaban Anda salah.</p>', unsafe_allow_html=True)
                st.write(f'Jawaban yang benar adalah {correct_option}')
                

        if next_button_clicked:
            st.session_state.randomized_images = get_randomized_images()
            st.session_state.randomized_options = None

if __name__ == '__main__':
    app()