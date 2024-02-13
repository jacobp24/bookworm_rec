```markdown
# Functional Specification

## Background:
We are creating an application to recommend books based on user input about the types of books they like.

## Example User Profiles

### Patrick's User Story:
- Avid lover of Agatha Christie
- He's read all of her books and needs an author with similar stories
- He wants to see a list of authors and top recommended books under each of them.
- He needs a user interface to look up books.
- He's not good with computers and wants a very simple UI that can spit out information with little input.

### Spongebob's User Story:
- Spongebob is an avid reader.
- He has read all the books published by his favorite author.
- He is hoping to find new books to read that are similar to his favorite books.
- [Stretch]: He would also like to know if they are available from his local library.
- He is good with computers.
- He expects any app he uses to return recommendations quickly.

## Data Sources:
- [Book Crossing Dataset](https://www.kaggle.com/datasets/ruchi798/bookcrossing-dataset/data)
  - BX-Book-Ratings.csv (1149779 values)
  - BX-Books.csv (271379 unique values)
- CMU Book Summary Dataset (16,559 unique values)

## Data Use Cases:

### Patrick's Use Case:
- **User:** Accesses recommendation tool
- **System:** Displays a drop down box asking how they want to search (Title, Author, Genre, Plot)
- **User:** Selects Title from the drop down box 
- **System:** Displays input box for Patrick to enter his favorite author 
- **System:** Displays optional filters (e.g. minimum star rating, genre)
- **User:** Patrick indicates that he only wants books that have at least three stars on average and have been reviewed by at least 4 people 
- **System:** Displays “Search Now” box
- **User:** Clicks “Search Now” box 
- **System:** Displays top 10 recommended books that are by Agatha Christi/similar to books by Agatha Christi and meet Patrick’s filter criteria 
- [Stretch]: Patrick clicks on a book that he likes and is provided with more details, such as whether the book is available through Seattle Public library 

### SpongeBob's Use Case:
- **User:** Accesses recommendation tool
- **System:** Displays a drop down box asking how they want to search (Title, Author, Genre, Plot)
- **User:** Clicks on “Learn More” to understand the difference between searching by Title, Author, Genre, or Plot 
- **System:** Displays popup box with instructions 
- **User:** Selects Genre from drop down box 
- **System:** Displays drop down box for available genres to search as well as “other” 
- **User:** Selects Mystery as the genre to search 
- **System:** Displays optional filters (e.g. minimum star rating)
- **User:** Sets all filters to none 
- **System:** Displays “Search Now” box 
- **User:** Clicks “Search Now” box 
- **System:** Gives the top 10 highest rated books in the Mystery genre, sorted by rating 
- [Stretch]: Spongebob clicks on a book that he likes and is provided with more details, such as whether the book is available through Seattle Public library 
```

