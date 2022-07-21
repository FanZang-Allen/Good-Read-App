import React from 'react'
import './Components.css';

const Author = ( { data }) => {
    const json_data = data;

    const name_str = json_data['author_name'] === undefined ? 'Unknown' : json_data['author_name'];
    const id_str = `(id: ${json_data['id']})`;

    const rating = json_data['rating'] === undefined ? 'Unknown' : json_data['rating'];
    const rating_str = `Average rating: ${rating} · `;

    const rating_count = json_data['rating_count'] === undefined ? 'Unknown' : json_data['rating_count'];
    const rating_count_str = `${rating_count} ratings · `;

    const review_count = json_data['review_count'] === undefined ? 'Unknown' : json_data['review_count'];
    const review_count_str = `${review_count} reviewers`;

    const author_url_str = json_data['author_url'] === undefined ? 'Unknown' : json_data['author_url'];

    const image_url_str = json_data['image_url'] === undefined ? 'Unknown' : json_data['image_url'];

    let author_books_str = '';
    if (json_data['author_books'] === undefined || json_data['author_books'].length === 0) {
        author_books_str = 'Unknown';
    } else {
        json_data['author_books'].forEach((book) => author_books_str += `"${book}" `)
    }

    let related_authors_str = '';
    if (json_data['related_authors'] === undefined || json_data['related_authors'].length === 0) {
        related_authors_str = 'Unknown';
    } else {
        json_data['related_authors'].forEach((author) => related_authors_str += `"${author}" `)
    }

    const unknown_image_src = "https://guidonpartners.com/wp-content/uploads/sites/15/2014/09/unknown.jpg";
    const image_src = image_url_str === 'Unknown' ? unknown_image_src : image_url_str;

    return (
        <div className='InfoContainer'>
            <img src={image_src} alt="" className='photo'/>
            <div className='DetailInfo'>
                <h3 style={{'color':'white'}}>{name_str + id_str}</h3>
                <h6 style={{'color':'white', 'fontSize':'15px'}}>{rating_str + rating_count_str + review_count_str}</h6>
                <p style={{'color':'white', 'fontSize':'12px'}}>
                    <span style={{'fontWeight': 'bold','fontSize':'15px'}}>
                        Author Books: </span>{author_books_str}<br/>
                    <span style={{'fontWeight': 'bold','fontSize':'15px'}}>
                        Related Authors: </span>{related_authors_str}<br/>
                    <span style={{'fontWeight': 'bold','fontSize':'15px'}}>
                        Main Page Url: </span>
                        <span style={{'color': 'blue'}}>
                        {author_url_str}</span><br/>
                    <span style={{'fontWeight': 'bold','fontSize':'15px'}}>
                        Image Url: </span>
                        <span style={{'color': 'blue'}}>
                        {image_url_str}</span>
                </p>
            </div>
        </div>
    )
}

export default Author
