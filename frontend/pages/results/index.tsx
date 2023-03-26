import Head from 'next/head'
import { withRouter } from 'next/router'
import { useRef, useState, useEffect } from 'react'

function Results({ router }: any) {
  // console.log(router)
  // console.log(JSON.parse(router.query.results))
  const [search, setSearch] = useState(router.query.search)
  const [results, setResults] = useState(JSON.parse(router.query.results))

  useEffect(() => {
    localStorage.setItem('search', JSON.stringify(search));
    localStorage.setItem('results', JSON.stringify(results));
  }, [search])

  useEffect(() => {
    // @ts-ignore
    const search = JSON.parse(localStorage.getItem('search'));
    // @ts-ignore
    const results = JSON.parse(localStorage.getItem('results'));
    if (search) setSearch(search);
    if (results) setResults(results);
  }, []);

  return (
    <>
      <Head>
        <title>Results</title>
        <link rel="icon" href="/favicon.png" />
      </Head>
      <main className='results'>
        <div className='header'>
          <span className="input-text">search: </span>
          <input type="text" className="textbox" placeholder={search} />
        </div>
        <div className='result-cards'>
          {
            results.map((e: any) => {
              return (
                <a href={e.url} className='card'>
                  <div className='title'>{e.title}</div>
                  <div className='url'>{e.url}</div>
                  <div className='description'>{e.description.split(' ').slice(0, 40).join(' ')}</div>
                </a>
              )
            })
          }
        </div>
      </main>
    </>
  )
}

export default withRouter(Results)
