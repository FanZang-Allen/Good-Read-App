import React from 'react'
import './Components.css';
import { useState } from "react";
import ErrorMessage from './ErrorMessage';

const PutMode = () => {

    let [bookMessage, setBookMessage] = useState('');
    let [authorMessage, setAuthorMessage] = useState('');

    async function UpdateBook(event) {
        event.preventDefault();
        let book_id = document.getElementById('book_id').value.trim();
        if (book_id === '') {
            setBookMessage('Please provide a book id');
            return
        }
        let data = {};
        const got_title = document.getElementById('book_title').value.trim();
        data['title'] = got_title === '' ? undefined : got_title;

        const got_isbn = document.getElementById('book_isbn').value.trim();
        data['ISBN'] = got_isbn === '' ? undefined : got_isbn;

        const got_rating = document.getElementById('book_rating').value.trim();
        data['rating'] = got_rating === '' ? undefined : got_rating;

        const got_rating_num = document.getElementById('book_rating_count').value.trim();
        data['rating_count'] = got_rating_num === '' ? undefined : got_rating_num;

        const got_review_num = document.getElementById('book_review_count').value.trim();
        data['review_count'] = got_review_num === '' ? undefined : got_review_num;

        const got_book_url = document.getElementById('book_url').value.trim();
        data['book_url'] = got_book_url === '' ? undefined : got_book_url;

        const got_image_url = document.getElementById('book_image_url').value.trim();
        data['image_url'] = got_image_url === '' ? undefined : got_image_url;

        const got_author_arr = document.getElementById('book_author').value.trim().split(',');
        data['author'] = got_author_arr[0] === '' ? undefined : got_author_arr;

        const got_author_url_arr = document.getElementById('book_author_url').value.trim().split(',');
        data['author_url'] = got_author_url_arr[0] === '' ? undefined : got_author_url_arr;

        const got_similar_book = document.getElementById('book_similar_book').value.trim().split(',');
        data['similar_books'] = got_similar_book[0] === '' ? undefined : got_similar_book;
        console.log(JSON.stringify(data));

        try {
            let response = await fetch(`http://127.0.0.1:5000/api/book?id=${book_id}`, {
                method: 'PUT',
                headers: {
                    'Content-Type': 'application/json' 
                },
                body: JSON.stringify(data)
            });
            if (response.status !== 200) {
                let error_data = await response.json();
                setBookMessage(error_data['error_message']);
            } else {
                let response_data = await response.json();
                setBookMessage(response_data['Response']);
            }
        } catch(e) {
            setBookMessage('Connection failed.');
            console.log(e);
        }
    }

    async function UpdateAuthor(event) {
        event.preventDefault();
        let author_id = document.getElementById('author_id').value.trim();
        if (author_id === '') {
            setAuthorMessage('Please provide a author id');
            return
        }
        let data = {};
        const got_name = document.getElementById('author_name').value.trim();
        data['author_name'] = got_name === '' ? undefined : got_name;

        const got_rating = document.getElementById('author_rating').value.trim();
        data['rating'] = got_rating === '' ? undefined : got_rating;

        const got_rating_num = document.getElementById('author_rating_count').value.trim();
        data['rating_count'] = got_rating_num === '' ? undefined : got_rating_num;

        const got_review_num = document.getElementById('author_review_count').value.trim();
        data['review_count'] = got_review_num === '' ? undefined : got_review_num;

        const got_author_url = document.getElementById('author_url').value.trim();
        data['author_url'] = got_author_url === '' ? undefined : got_author_url;

        const got_image_url = document.getElementById('author_image_url').value.trim();
        data['image_url'] = got_image_url === '' ? undefined : got_image_url;

        const got_author_arr = document.getElementById('related_author').value.trim().split(',');
        data['related_authors'] = got_author_arr[0] === '' ? undefined : got_author_arr;

        const got_book_arr = document.getElementById('author_book').value.trim().split(',');
        data['author_books'] = got_book_arr[0] === '' ? undefined : got_book_arr;

        console.log(JSON.stringify(data));

        try {
            let response = await fetch(`http://127.0.0.1:5000/api/author?id=${author_id}`, {
                method: 'PUT',
                headers: {
                    'Content-Type': 'application/json' 
                },
                body: JSON.stringify(data)
            });
            if (response.status !== 200) {
                let error_data = await response.json();
                setAuthorMessage(error_data['error_message']);
            } else {
                let response_data = await response.json();
                setAuthorMessage(response_data['Response']);
            }
        } catch(e) {
            setAuthorMessage('Connection failed.');
            console.log(e);
        }
    }

    return (
        <div className='VerticalCenterContainer'>
            <h1 className='Header'style = {{margin: 10}}> Update Book</h1>
            <form className="InputHolder">
                <div className="Input">
                    <h2 className='QueryArgString'> ID:</h2>
                    <input
                        type='text'
                        style = {{"width": "15%"}}
                        placeholder= 'Required'
                        id = 'book_id'
                    />
                    <h2 className='QueryArgString' > Title:</h2>
                    <input
                        type='text'
                        style = {{"width": "40%"}}
                        placeholder= 'ex.The Pragmatic Programmer'
                        id = 'book_title'
                    />
                    <h2 className='QueryArgString'> ISBN:</h2>
                    <input
                        type='text'
                        style = {{"width": "15%"}}
                        placeholder= 'ex.161622'
                        id = 'book_isbn'
                    />
                </div>
            </form>
            <form className="InputHolder">
                <div className="Input">
                    <h2 className='QueryArgString'> Rating:</h2>
                    <input
                        type='text'
                        style = {{"width": "100px"}}
                        placeholder= 'ex. 4.23'
                        id = 'book_rating'
                    />
                    <h2 className='QueryArgString'> Rating Num:</h2>
                    <input
                        type='text'
                        style = {{"width": "110px"}}
                        placeholder= 'ex.45623'
                        id = 'book_rating_count'
                    />
                    <h2 className='QueryArgString'> Review Num:</h2>
                    <input
                        type='text'
                        style = {{"width": "110px"}}
                        placeholder= 'ex.3983'
                        id = 'book_review_count'
                    />
                </div>
            </form>
            <form className="InputHolder">
                <div className="Input">
                    <h2 className='QueryArgString'> Author:</h2>
                    <input
                        type='text'
                        style = {{"width": '530px'}}
                        placeholder= 'ex. Andy Hunt,Dave Thomas'
                        id = 'book_author'
                    />
                </div>
            </form>
            <form className="InputHolder">
                <div className="Input">
                    <h2 className='QueryArgString'> Author Url:</h2>
                    <input
                        type='text'
                        style = {{"width": '510px'}}
                        placeholder= 'ex.first url,second url'
                        id = 'book_author_url'
                    />
                </div>
            </form>
            <form className="InputHolder">
                <div className="Input">
                    <h2 className='QueryArgString'> Book Url:</h2>
                    <input
                        type='text'
                        style = {{"width": '520px'}}
                        placeholder= 'ex.https://www.goodreads.com/book/*'
                        id = 'book_url'
                    />
                </div>
            </form>
            <form className="InputHolder">
                <div className="Input">
                    <h2 className='QueryArgString'> Image Url:</h2>
                    <input
                        type='text'
                        style = {{"width": '510px'}}
                        placeholder= 'ex.https://*.jpg'
                        id = 'book_image_url'
                    />
                </div>
            </form>
            <form className="InputHolder">
                <div className="Input">
                    <h2 className='QueryArgString'> Similar Books:</h2>
                    <input
                        type='text'
                        style = {{"width": '480px'}}
                        placeholder= 'ex. Book1,Book2,Book3'
                        id = 'book_similar_book'
                    />
                </div>
            </form>
            <button className='Button' onClick={UpdateBook}>Update</button>
            <div id='bookMessage'><ErrorMessage message={bookMessage}/></div>

            <h1 className='Header'style = {{margin: 10}}> Update Author</h1>
            <form className="InputHolder">
                <div className="Input">
                    <h2 className='QueryArgString'> ID:</h2>
                    <input
                        type='text'
                        style = {{"width": "250px"}}
                        placeholder= 'Required'
                        id = 'author_id'
                    />
                    <h2 className='QueryArgString' > Name:</h2>
                    <input
                        type='text'
                        style = {{"width": "250px"}}
                        placeholder= 'ex.Andy Hunt'
                        id = 'author_name'
                    />
                </div>
            </form>
            <form className="InputHolder">
                <div className="Input">
                    <h2 className='QueryArgString'> Rating:</h2>
                    <input
                        type='text'
                        style = {{"width": "100px"}}
                        placeholder= 'ex. 4.23'
                        id = 'author_rating'
                    />
                    <h2 className='QueryArgString'> Rating Num:</h2>
                    <input
                        type='text'
                        style = {{"width": "110px"}}
                        placeholder= 'ex.45623'
                        id = 'author_rating_count'
                    />
                    <h2 className='QueryArgString'> Review Num:</h2>
                    <input
                        type='text'
                        style = {{"width": "110px"}}
                        placeholder= 'ex.3983'
                        id = 'author_review_count'
                    />
                </div>
            </form>
            <form className="InputHolder">
                <div className="Input">
                    <h2 className='QueryArgString'> Main Page Url:</h2>
                    <input
                        type='text'
                        style = {{"width": '480px'}}
                        placeholder= 'ex.https://www.goodreads.com/author/*'
                        id = 'author_url'
                    />
                </div>
            </form>
            <form className="InputHolder">
                <div className="Input">
                    <h2 className='QueryArgString'> Image Url:</h2>
                    <input
                        type='text'
                        style = {{"width": '510px'}}
                        placeholder= 'ex.https://*.jpg'
                        id = 'author_image_url'
                    />
                </div>
            </form>
            <form className="InputHolder">
                <div className="Input">
                    <h2 className='QueryArgString'> Author Books:</h2>
                    <input
                        type='text'
                        style = {{"width": '480px'}}
                        placeholder= 'ex. Book1,Book2,Book3'
                        id = 'author_book'
                    />
                </div>
            </form>
            <form className="InputHolder">
                <div className="Input">
                    <h2 className='QueryArgString'> Related Authors:</h2>
                    <input
                        type='text'
                        style = {{"width": '460px'}}
                        placeholder= 'ex. Author1,Author2,Author3'
                        id = 'related_author'
                    />
                </div>
            </form>
            <button className='Button' onClick={UpdateAuthor}>Update</button>
            <div id='authorMessage'><ErrorMessage message={authorMessage}/></div>
        </div>
    )
}

export default PutMode
