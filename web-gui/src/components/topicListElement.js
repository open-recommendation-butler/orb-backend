import React, { useState } from 'react';
import ArticleListElement from './articleListElement';
import { useSearchParams } from "react-router-dom";

function TopicListElement({ topic }) {
  let [searchParams] = useSearchParams();
  const [showFull, setShowFull] = useState(false);

  return (
    <div className='mb-4 border-b border-slate-300 py-1'>
      <p className='text-m font-bold'>{topic.keywords.slice(0,3).map((keyword, index) => 
        <>
          {index !== 0 ? ', ' : ''}
          <a className='hover:underline' href={`/search?q=${keyword}${searchParams.get('content_type') ? '&content_type=' + searchParams.get('content_type') : ''}${searchParams.get('publisher') ? '&publisher=' + searchParams.get('publisher') : ''}${searchParams.get('category') ? '&category=' + searchParams.get('category') : ''}`}>{keyword}</a>
        </>
      )}</p>
      {topic.article_count && topic.article_count > 1
        ? 
          <>
            <div className='grid md:grid-cols-2 gap-x-5'>
              {topic.articles.slice(0,showFull ? 999 : 4).map(article => <ArticleListElement article={article} />)}
            </div>
            {topic.article_count > 4 &&
              <button className='text-center flex items-center mx-auto hover:underline text-sm my-1' onClick={() => setShowFull(!showFull)}>
                {showFull ? "Show less" : "Show more"}
                <svg className={`ml-1 transition-all duration-300 ${showFull && 'rotate-180'}`} width="9" height="7" viewBox="0 0 172 149" fill="none" xmlns="http://www.w3.org/2000/svg">
                  <path d="M86 149L0.263502 0.499984L171.737 0.499999L86 149Z" fill="black"/>
                </svg>
              </button>
            }
          </>
        : <ArticleListElement article={topic.articles ? topic.articles[0] : topic} />
      }
    </div>
  )
}

export default TopicListElement;