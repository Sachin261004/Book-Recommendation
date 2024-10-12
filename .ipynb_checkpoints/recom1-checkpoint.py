{
 "cells": [
  {
   "cell_type": "code",
   "execution_count": 1,
   "metadata": {},
   "outputs": [],
   "source": [
    "import pandas as pd\n",
    "from sklearn.metrics.pairwise import cosine_similarity\n",
    "from sklearn.feature_extraction.text import TfidfVectorizer\n",
    "from sklearn.neighbors import NearestNeighbors"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": 2,
   "metadata": {},
   "outputs": [
    {
     "name": "stderr",
     "output_type": "stream",
     "text": [
      "C:\\Users\\sachi\\AppData\\Local\\Temp\\ipykernel_24544\\1445278838.py:1: DtypeWarning: Columns (3) have mixed types. Specify dtype option on import or set low_memory=False.\n",
      "  books = pd.read_csv('archive/Books.csv')\n"
     ]
    }
   ],
   "source": [
    "books = pd.read_csv('archive/Books.csv')\n",
    "users = pd.read_csv('archive/Users.csv')\n",
    "ratings = pd.read_csv('archive/Ratings.csv')"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": 17,
   "metadata": {},
   "outputs": [
    {
     "data": {
      "text/plain": [
       "ISBN                   0\n",
       "Book-Title             0\n",
       "Book-Author            2\n",
       "Year-Of-Publication    0\n",
       "Publisher              2\n",
       "Image-URL-S            0\n",
       "Image-URL-M            0\n",
       "Image-URL-L            3\n",
       "combined_features      0\n",
       "dtype: int64"
      ]
     },
     "execution_count": 17,
     "metadata": {},
     "output_type": "execute_result"
    }
   ],
   "source": [
    "books.isnull().sum()"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": 4,
   "metadata": {},
   "outputs": [
    {
     "data": {
      "text/plain": [
       "User-ID        0\n",
       "ISBN           0\n",
       "Book-Rating    0\n",
       "dtype: int64"
      ]
     },
     "execution_count": 4,
     "metadata": {},
     "output_type": "execute_result"
    }
   ],
   "source": [
    "ratings.isnull().sum()"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": 5,
   "metadata": {},
   "outputs": [
    {
     "data": {
      "text/plain": [
       "0"
      ]
     },
     "execution_count": 5,
     "metadata": {},
     "output_type": "execute_result"
    }
   ],
   "source": [
    "books.duplicated().sum()"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": 6,
   "metadata": {},
   "outputs": [
    {
     "data": {
      "text/plain": [
       "0"
      ]
     },
     "execution_count": 6,
     "metadata": {},
     "output_type": "execute_result"
    }
   ],
   "source": [
    "ratings.duplicated().sum()"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": 7,
   "metadata": {},
   "outputs": [
    {
     "data": {
      "text/plain": [
       "User-ID                0\n",
       "ISBN                   0\n",
       "Book-Rating            0\n",
       "Book-Title             0\n",
       "Book-Author            2\n",
       "Year-Of-Publication    0\n",
       "Publisher              2\n",
       "Image-URL-S            0\n",
       "Image-URL-M            0\n",
       "Image-URL-L            4\n",
       "dtype: int64"
      ]
     },
     "execution_count": 7,
     "metadata": {},
     "output_type": "execute_result"
    }
   ],
   "source": [
    "ratings_books = pd.merge(ratings, books, on='ISBN')\n",
    "ratings_books.isnull().sum()"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": 8,
   "metadata": {},
   "outputs": [],
   "source": [
    "user_prune = ratings_books.groupby('User-ID')['Book-Rating'].count() > 100\n",
    "user_and_rating = user_prune[user_prune].index "
   ]
  },
  {
   "cell_type": "code",
   "execution_count": 9,
   "metadata": {},
   "outputs": [
    {
     "data": {
      "text/plain": [
       "User-ID                0\n",
       "ISBN                   0\n",
       "Book-Rating            0\n",
       "Book-Title             0\n",
       "Book-Author            0\n",
       "Year-Of-Publication    0\n",
       "Publisher              0\n",
       "Image-URL-S            0\n",
       "Image-URL-M            0\n",
       "Image-URL-L            0\n",
       "dtype: int64"
      ]
     },
     "execution_count": 9,
     "metadata": {},
     "output_type": "execute_result"
    }
   ],
   "source": [
    "filtered_rating = ratings_books[ratings_books['User-ID'].isin(user_and_rating)]\n",
    "\n",
    "rating_prune = ratings_books.groupby('Book-Title')['Book-Rating'].count() >= 50\n",
    "famous_books = rating_prune[rating_prune].index\n",
    "\n",
    "final_rating = filtered_rating[filtered_rating['Book-Title'].isin(famous_books)]\n",
    "final_rating.isnull().sum()"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": 10,
   "metadata": {},
   "outputs": [
    {
     "data": {
      "text/html": [
       "<div>\n",
       "<style scoped>\n",
       "    .dataframe tbody tr th:only-of-type {\n",
       "        vertical-align: middle;\n",
       "    }\n",
       "\n",
       "    .dataframe tbody tr th {\n",
       "        vertical-align: top;\n",
       "    }\n",
       "\n",
       "    .dataframe thead th {\n",
       "        text-align: right;\n",
       "    }\n",
       "</style>\n",
       "<table border=\"1\" class=\"dataframe\">\n",
       "  <thead>\n",
       "    <tr style=\"text-align: right;\">\n",
       "      <th></th>\n",
       "      <th>User-ID</th>\n",
       "      <th>ISBN</th>\n",
       "      <th>Book-Rating</th>\n",
       "      <th>Book-Title</th>\n",
       "      <th>Book-Author</th>\n",
       "      <th>Year-Of-Publication</th>\n",
       "      <th>Publisher</th>\n",
       "      <th>Image-URL-S</th>\n",
       "      <th>Image-URL-M</th>\n",
       "      <th>Image-URL-L</th>\n",
       "    </tr>\n",
       "  </thead>\n",
       "  <tbody>\n",
       "    <tr>\n",
       "      <th>2</th>\n",
       "      <td>6543</td>\n",
       "      <td>034545104X</td>\n",
       "      <td>0</td>\n",
       "      <td>Flesh Tones: A Novel</td>\n",
       "      <td>M. J. Rose</td>\n",
       "      <td>2002</td>\n",
       "      <td>Ballantine Books</td>\n",
       "      <td>http://images.amazon.com/images/P/034545104X.0...</td>\n",
       "      <td>http://images.amazon.com/images/P/034545104X.0...</td>\n",
       "      <td>http://images.amazon.com/images/P/034545104X.0...</td>\n",
       "    </tr>\n",
       "    <tr>\n",
       "      <th>4</th>\n",
       "      <td>10314</td>\n",
       "      <td>034545104X</td>\n",
       "      <td>9</td>\n",
       "      <td>Flesh Tones: A Novel</td>\n",
       "      <td>M. J. Rose</td>\n",
       "      <td>2002</td>\n",
       "      <td>Ballantine Books</td>\n",
       "      <td>http://images.amazon.com/images/P/034545104X.0...</td>\n",
       "      <td>http://images.amazon.com/images/P/034545104X.0...</td>\n",
       "      <td>http://images.amazon.com/images/P/034545104X.0...</td>\n",
       "    </tr>\n",
       "    <tr>\n",
       "      <th>5</th>\n",
       "      <td>23768</td>\n",
       "      <td>034545104X</td>\n",
       "      <td>0</td>\n",
       "      <td>Flesh Tones: A Novel</td>\n",
       "      <td>M. J. Rose</td>\n",
       "      <td>2002</td>\n",
       "      <td>Ballantine Books</td>\n",
       "      <td>http://images.amazon.com/images/P/034545104X.0...</td>\n",
       "      <td>http://images.amazon.com/images/P/034545104X.0...</td>\n",
       "      <td>http://images.amazon.com/images/P/034545104X.0...</td>\n",
       "    </tr>\n",
       "    <tr>\n",
       "      <th>7</th>\n",
       "      <td>28523</td>\n",
       "      <td>034545104X</td>\n",
       "      <td>0</td>\n",
       "      <td>Flesh Tones: A Novel</td>\n",
       "      <td>M. J. Rose</td>\n",
       "      <td>2002</td>\n",
       "      <td>Ballantine Books</td>\n",
       "      <td>http://images.amazon.com/images/P/034545104X.0...</td>\n",
       "      <td>http://images.amazon.com/images/P/034545104X.0...</td>\n",
       "      <td>http://images.amazon.com/images/P/034545104X.0...</td>\n",
       "    </tr>\n",
       "    <tr>\n",
       "      <th>14</th>\n",
       "      <td>77480</td>\n",
       "      <td>034545104X</td>\n",
       "      <td>8</td>\n",
       "      <td>Flesh Tones: A Novel</td>\n",
       "      <td>M. J. Rose</td>\n",
       "      <td>2002</td>\n",
       "      <td>Ballantine Books</td>\n",
       "      <td>http://images.amazon.com/images/P/034545104X.0...</td>\n",
       "      <td>http://images.amazon.com/images/P/034545104X.0...</td>\n",
       "      <td>http://images.amazon.com/images/P/034545104X.0...</td>\n",
       "    </tr>\n",
       "  </tbody>\n",
       "</table>\n",
       "</div>"
      ],
      "text/plain": [
       "    User-ID        ISBN  Book-Rating            Book-Title Book-Author  \\\n",
       "2      6543  034545104X            0  Flesh Tones: A Novel  M. J. Rose   \n",
       "4     10314  034545104X            9  Flesh Tones: A Novel  M. J. Rose   \n",
       "5     23768  034545104X            0  Flesh Tones: A Novel  M. J. Rose   \n",
       "7     28523  034545104X            0  Flesh Tones: A Novel  M. J. Rose   \n",
       "14    77480  034545104X            8  Flesh Tones: A Novel  M. J. Rose   \n",
       "\n",
       "   Year-Of-Publication         Publisher  \\\n",
       "2                 2002  Ballantine Books   \n",
       "4                 2002  Ballantine Books   \n",
       "5                 2002  Ballantine Books   \n",
       "7                 2002  Ballantine Books   \n",
       "14                2002  Ballantine Books   \n",
       "\n",
       "                                          Image-URL-S  \\\n",
       "2   http://images.amazon.com/images/P/034545104X.0...   \n",
       "4   http://images.amazon.com/images/P/034545104X.0...   \n",
       "5   http://images.amazon.com/images/P/034545104X.0...   \n",
       "7   http://images.amazon.com/images/P/034545104X.0...   \n",
       "14  http://images.amazon.com/images/P/034545104X.0...   \n",
       "\n",
       "                                          Image-URL-M  \\\n",
       "2   http://images.amazon.com/images/P/034545104X.0...   \n",
       "4   http://images.amazon.com/images/P/034545104X.0...   \n",
       "5   http://images.amazon.com/images/P/034545104X.0...   \n",
       "7   http://images.amazon.com/images/P/034545104X.0...   \n",
       "14  http://images.amazon.com/images/P/034545104X.0...   \n",
       "\n",
       "                                          Image-URL-L  \n",
       "2   http://images.amazon.com/images/P/034545104X.0...  \n",
       "4   http://images.amazon.com/images/P/034545104X.0...  \n",
       "5   http://images.amazon.com/images/P/034545104X.0...  \n",
       "7   http://images.amazon.com/images/P/034545104X.0...  \n",
       "14  http://images.amazon.com/images/P/034545104X.0...  "
      ]
     },
     "execution_count": 10,
     "metadata": {},
     "output_type": "execute_result"
    }
   ],
   "source": [
    "final_rating.head()"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": 11,
   "metadata": {},
   "outputs": [],
   "source": [
    "user_item_matrix = final_rating.pivot_table(index='User-ID', columns='Book-Title', values='Book-Rating')\n",
    "user_item_matrix.fillna(0, inplace=True)\n",
    "user_similarity = cosine_similarity(user_item_matrix)\n",
    "user_similarity_df = pd.DataFrame(user_similarity, index=user_item_matrix.index, columns=user_item_matrix.index)\n"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": 12,
   "metadata": {},
   "outputs": [],
   "source": [
    "#user based\n",
    "def recommend_books_collaborative(user_id, num_recommendations=5):\n",
    "    similar_users = user_similarity_df[user_id].sort_values(ascending=False).index[1:]\n",
    "    similar_user_ratings = user_item_matrix.loc[similar_users]\n",
    "    user_ratings = user_item_matrix.loc[user_id]\n",
    "    recommended_books = similar_user_ratings.loc[:, user_ratings == 0].mean().sort_values(ascending=False).head(num_recommendations)\n",
    "    return recommended_books.index.tolist()"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": 13,
   "metadata": {},
   "outputs": [
    {
     "data": {
      "text/html": [
       "<style>#sk-container-id-1 {color: black;background-color: white;}#sk-container-id-1 pre{padding: 0;}#sk-container-id-1 div.sk-toggleable {background-color: white;}#sk-container-id-1 label.sk-toggleable__label {cursor: pointer;display: block;width: 100%;margin-bottom: 0;padding: 0.3em;box-sizing: border-box;text-align: center;}#sk-container-id-1 label.sk-toggleable__label-arrow:before {content: \"▸\";float: left;margin-right: 0.25em;color: #696969;}#sk-container-id-1 label.sk-toggleable__label-arrow:hover:before {color: black;}#sk-container-id-1 div.sk-estimator:hover label.sk-toggleable__label-arrow:before {color: black;}#sk-container-id-1 div.sk-toggleable__content {max-height: 0;max-width: 0;overflow: hidden;text-align: left;background-color: #f0f8ff;}#sk-container-id-1 div.sk-toggleable__content pre {margin: 0.2em;color: black;border-radius: 0.25em;background-color: #f0f8ff;}#sk-container-id-1 input.sk-toggleable__control:checked~div.sk-toggleable__content {max-height: 200px;max-width: 100%;overflow: auto;}#sk-container-id-1 input.sk-toggleable__control:checked~label.sk-toggleable__label-arrow:before {content: \"▾\";}#sk-container-id-1 div.sk-estimator input.sk-toggleable__control:checked~label.sk-toggleable__label {background-color: #d4ebff;}#sk-container-id-1 div.sk-label input.sk-toggleable__control:checked~label.sk-toggleable__label {background-color: #d4ebff;}#sk-container-id-1 input.sk-hidden--visually {border: 0;clip: rect(1px 1px 1px 1px);clip: rect(1px, 1px, 1px, 1px);height: 1px;margin: -1px;overflow: hidden;padding: 0;position: absolute;width: 1px;}#sk-container-id-1 div.sk-estimator {font-family: monospace;background-color: #f0f8ff;border: 1px dotted black;border-radius: 0.25em;box-sizing: border-box;margin-bottom: 0.5em;}#sk-container-id-1 div.sk-estimator:hover {background-color: #d4ebff;}#sk-container-id-1 div.sk-parallel-item::after {content: \"\";width: 100%;border-bottom: 1px solid gray;flex-grow: 1;}#sk-container-id-1 div.sk-label:hover label.sk-toggleable__label {background-color: #d4ebff;}#sk-container-id-1 div.sk-serial::before {content: \"\";position: absolute;border-left: 1px solid gray;box-sizing: border-box;top: 0;bottom: 0;left: 50%;z-index: 0;}#sk-container-id-1 div.sk-serial {display: flex;flex-direction: column;align-items: center;background-color: white;padding-right: 0.2em;padding-left: 0.2em;position: relative;}#sk-container-id-1 div.sk-item {position: relative;z-index: 1;}#sk-container-id-1 div.sk-parallel {display: flex;align-items: stretch;justify-content: center;background-color: white;position: relative;}#sk-container-id-1 div.sk-item::before, #sk-container-id-1 div.sk-parallel-item::before {content: \"\";position: absolute;border-left: 1px solid gray;box-sizing: border-box;top: 0;bottom: 0;left: 50%;z-index: -1;}#sk-container-id-1 div.sk-parallel-item {display: flex;flex-direction: column;z-index: 1;position: relative;background-color: white;}#sk-container-id-1 div.sk-parallel-item:first-child::after {align-self: flex-end;width: 50%;}#sk-container-id-1 div.sk-parallel-item:last-child::after {align-self: flex-start;width: 50%;}#sk-container-id-1 div.sk-parallel-item:only-child::after {width: 0;}#sk-container-id-1 div.sk-dashed-wrapped {border: 1px dashed gray;margin: 0 0.4em 0.5em 0.4em;box-sizing: border-box;padding-bottom: 0.4em;background-color: white;}#sk-container-id-1 div.sk-label label {font-family: monospace;font-weight: bold;display: inline-block;line-height: 1.2em;}#sk-container-id-1 div.sk-label-container {text-align: center;}#sk-container-id-1 div.sk-container {/* jupyter's `normalize.less` sets `[hidden] { display: none; }` but bootstrap.min.css set `[hidden] { display: none !important; }` so we also need the `!important` here to be able to override the default hidden behavior on the sphinx rendered scikit-learn.org. See: https://github.com/scikit-learn/scikit-learn/issues/21755 */display: inline-block !important;position: relative;}#sk-container-id-1 div.sk-text-repr-fallback {display: none;}</style><div id=\"sk-container-id-1\" class=\"sk-top-container\"><div class=\"sk-text-repr-fallback\"><pre>NearestNeighbors(algorithm=&#x27;brute&#x27;, metric=&#x27;cosine&#x27;, n_neighbors=6)</pre><b>In a Jupyter environment, please rerun this cell to show the HTML representation or trust the notebook. <br />On GitHub, the HTML representation is unable to render, please try loading this page with nbviewer.org.</b></div><div class=\"sk-container\" hidden><div class=\"sk-item\"><div class=\"sk-estimator sk-toggleable\"><input class=\"sk-toggleable__control sk-hidden--visually\" id=\"sk-estimator-id-1\" type=\"checkbox\" checked><label for=\"sk-estimator-id-1\" class=\"sk-toggleable__label sk-toggleable__label-arrow\">NearestNeighbors</label><div class=\"sk-toggleable__content\"><pre>NearestNeighbors(algorithm=&#x27;brute&#x27;, metric=&#x27;cosine&#x27;, n_neighbors=6)</pre></div></div></div></div></div>"
      ],
      "text/plain": [
       "NearestNeighbors(algorithm='brute', metric='cosine', n_neighbors=6)"
      ]
     },
     "execution_count": 13,
     "metadata": {},
     "output_type": "execute_result"
    }
   ],
   "source": [
    "#content based\n",
    "books['combined_features'] = books['Book-Title'].fillna('') + \" \" + books['Book-Author'].fillna('') + \" \" + books['Publisher'].fillna('')\n",
    "tfidf = TfidfVectorizer(stop_words='english')\n",
    "tfidf_matrix = tfidf.fit_transform(books['combined_features'])\n",
    "nn = NearestNeighbors(metric='cosine', algorithm='brute', n_neighbors=6)\n",
    "nn.fit(tfidf_matrix)"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": 14,
   "metadata": {},
   "outputs": [],
   "source": [
    "def recommend_books_content_based(book_title, num_recommendations=5):\n",
    "    if book_title in books['Book-Title'].values:\n",
    "        book_idx = books[books['Book-Title'] == book_title].index[0]\n",
    "        distances, indices = nn.kneighbors(tfidf_matrix[book_idx], n_neighbors=num_recommendations+1)\n",
    "        book_indices = indices.flatten()[1:]\n",
    "        return books['Book-Title'].iloc[book_indices].tolist()\n",
    "    else:\n",
    "        return [\"The book title '{}' does not exist in the dataset.\".format(book_title)]\n"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": 15,
   "metadata": {},
   "outputs": [],
   "source": [
    "def hybrid_recommendation(user_id, book_title, num_recommendations=5):\n",
    "    collaborative_recommendations = recommend_books_collaborative(user_id, num_recommendations)\n",
    "    content_based_recommendations = recommend_books_content_based(book_title, num_recommendations)\n",
    "    \n",
    "    if isinstance(content_based_recommendations, list) and \"does not exist in the dataset\" in content_based_recommendations[0]:\n",
    "        content_based_recommendations = recommend_books_content_based(collaborative_recommendations[0], num_recommendations)\n",
    "    \n",
    "    final_recommendations = list(set(collaborative_recommendations + content_based_recommendations))\n",
    "    return final_recommendations[:num_recommendations]\n"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": 20,
   "metadata": {},
   "outputs": [
    {
     "name": "stdout",
     "output_type": "stream",
     "text": [
      "Collaborative Filtering Recommendations:\n",
      "['The Lovely Bones: A Novel', 'Harry Potter and the Chamber of Secrets (Book 2)', 'Harry Potter and the Prisoner of Azkaban (Book 3)', 'The Secret Life of Bees', \"Harry Potter and the Sorcerer's Stone (Harry Potter (Paperback))\"]\n",
      "\n",
      "Content-Based Recommendations:\n",
      "['Classical mythology', 'Classical mythology', 'Classical Mythology', \"Who's Who in Classical Mythology (Who's Who Series)\", 'The Oxford Classical Dictionary']\n",
      "\n",
      "Hybrid Recommendations:\n",
      "['Harry Potter and the Chamber of Secrets (Book 2)', 'Harry Potter and the Prisoner of Azkaban (Book 3)', 'The Secret Life of Bees', 'Classical Mythology', 'Classical mythology']\n"
     ]
    }
   ],
   "source": [
    "user_id_example = 277427\n",
    "book_title_example = \"Classical Mythology\"\n",
    "\n",
    "print(\"Collaborative Filtering Recommendations:\")\n",
    "print(recommend_books_collaborative(user_id_example))\n",
    "\n",
    "print(\"\\nContent-Based Recommendations:\")\n",
    "print(recommend_books_content_based(book_title_example))\n",
    "\n",
    "print(\"\\nHybrid Recommendations:\")\n",
    "print(hybrid_recommendation(user_id_example, book_title_example))"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": 25,
   "metadata": {},
   "outputs": [
    {
     "name": "stdout",
     "output_type": "stream",
     "text": [
      "Collaborative Filtering Recommendations:\n",
      "['The Lovely Bones: A Novel', 'Harry Potter and the Chamber of Secrets (Book 2)', 'Harry Potter and the Prisoner of Azkaban (Book 3)', 'The Secret Life of Bees', \"Harry Potter and the Sorcerer's Stone (Harry Potter (Paperback))\"]\n",
      "\n",
      "Content-Based Recommendations:\n",
      "['Pleading Guilty', 'Pleading Guilty', 'Pleading Guilty (G K Hall Large Print Book Series)', 'GUILTY AS CHARGED', 'The BURDEN OF PROOF']\n",
      "\n",
      "Hybrid Recommendations:\n",
      "['Harry Potter and the Chamber of Secrets (Book 2)', 'Harry Potter and the Prisoner of Azkaban (Book 3)', 'The Secret Life of Bees', 'Pleading Guilty', 'GUILTY AS CHARGED']\n"
     ]
    }
   ],
   "source": [
    "user_id_example = 277427\n",
    "book_title_example = \"PLEADING GUILTY\"\n",
    "\n",
    "print(\"Collaborative Filtering Recommendations:\")\n",
    "print(recommend_books_collaborative(user_id_example))\n",
    "\n",
    "print(\"\\nContent-Based Recommendations:\")\n",
    "print(recommend_books_content_based(book_title_example))\n",
    "\n",
    "print(\"\\nHybrid Recommendations:\")\n",
    "print(hybrid_recommendation(user_id_example, book_title_example))"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": null,
   "metadata": {},
   "outputs": [],
   "source": []
  }
 ],
 "metadata": {
  "kernelspec": {
   "display_name": "Python 3 (ipykernel)",
   "language": "python",
   "name": "python3"
  },
  "language_info": {
   "codemirror_mode": {
    "name": "ipython",
    "version": 3
   },
   "file_extension": ".py",
   "mimetype": "text/x-python",
   "name": "python",
   "nbconvert_exporter": "python",
   "pygments_lexer": "ipython3",
   "version": "3.11.7"
  }
 },
 "nbformat": 4,
 "nbformat_minor": 4
}
