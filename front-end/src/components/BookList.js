import React from 'react'
import Book from './Book'

const BookList = ( { infolist }) => {
    return (
        <>
        {infolist.map((info) => (
            <Book data={info}/>
        ))}
        </>
    )
}

export default BookList
