import React from 'react';
import './Components.css';

const Book = ( { data }) => {
    const json_data = data;

    const name_str = json_data['title'] === undefined ? 'Unknown' : json_data['title'];
    const id_str = `(id: ${json_data['id']})`;

    const isbn_str = json_data['ISBN'] === undefined ? 'Unknown' : json_data['ISBN'];

    const rating = json_data['rating'] === undefined ? 'Unknown' : json_data['rating'];
    const rating_str = `Average rating: ${rating} · `;

    const rating_count = json_data['rating_count'] === undefined ? 'Unknown' : json_data['rating_count'];
    const rating_count_str = `${rating_count} ratings · `;

    const review_count = json_data['review_count'] === undefined ? 'Unknown' : json_data['review_count'];
    const review_count_str = `${review_count} reviewers`;

    const book_url_str = json_data['book_url'] === undefined ? 'Unknown' : json_data['book_url'];

    let author_block = '';
    if (json_data['author'] === undefined || json_data['author'].length === 0) {
        author_block = 'Unknown';
    } else {
        json_data['author'].forEach((author) => author_block += `${author}, `)
        author_block = author_block.slice(0, -2) + '.';
    }

    let author_url_block = '';
    if (json_data['author_url'] === undefined || json_data['author_url'].length === 0) {
        author_url_block = 'Unknown';
    } else {
        json_data['author_url'].forEach((url) => author_url_block += `${url}, `)
        author_url_block = author_url_block.slice(0, -2);
    }

    let similar_books_str = '';
    if (json_data['similar_books'] === undefined || json_data['similar_books'].length === 0) {
        similar_books_str = 'Unknown';
    } else {
        json_data['similar_books'].forEach((book) => similar_books_str += `"${book}" `)
    }

    const image_url_str = json_data['image_url'] === undefined ? 'Unknown' : json_data['image_url'];
    const unknown_image_src = "https://web.extension.illinois.edu/stain/stains-hi/235.jpg";
    const image_src = image_url_str === 'Unknown' ? unknown_image_src : image_url_str;

    return (
        <div className='InfoContainer'>
            <img src={image_src} alt="" className='photo'/>
            <div className='DetailInfo'>
                <h3 style={{'color':'white'}}>{name_str + id_str}</h3>
                <h6 style={{'color':'white', 'fontSize':'15px'}}>{rating_str + rating_count_str + review_count_str}</h6>
                <p style={{'color':'white', 'fontSize':'12px'}}>
                    <span style={{'fontWeight': 'bold','fontSize':'15px'}}>
                        Authors: </span>{author_block}<br/>
                    <span style={{'fontWeight': 'bold','fontSize':'15px'}}>
                        Authors Url: </span><br/>
                        <span style={{'color': 'blue'}}>
                        {author_url_block}</span><br/>
                    <span style={{'fontWeight': 'bold','fontSize':'15px'}}>
                        ISBN: </span>{isbn_str}<br/>
                    <span style={{'fontWeight': 'bold','fontSize':'15px'}}>
                        Similar Books: </span>{similar_books_str}<br/>
                    <span style={{'fontWeight': 'bold','fontSize':'15px'}}>
                        Book Url: </span>
                        <span style={{'color': 'blue'}}>
                        {book_url_str}</span><br/>
                    <span style={{'fontWeight': 'bold','fontSize':'15px'}}>
                        Image Url: </span>
                        <span style={{'color': 'blue'}}>
                        {image_url_str}</span>
                </p>
            </div>
        </div>
    )
}

export default Book
