import Head from 'next/head'
import { useRef, useState, useEffect } from 'react'
import axios from 'axios'
import { useRouter } from 'next/router'


export default function Home() {
  const inputRef = useRef(null);
  const router = useRouter()
  const [search, setSearch] = useState('')
  
  useEffect(() => {
    // @ts-ignore
    inputRef.current.focus();
  }, [])
  
  function handleChange(e: any) {
    const { value } = e.target;
    setSearch(value);
    console.log(search)
  }

  async function onKeyDown(e: any){
    if (e.key === 'Enter'){
      let res : any = await axios.post(
        `${process.env.NEXT_PUBLIC_API}`, {
        "search": search
      });

      router.push({
        pathname: "/results",
        query: {
          "search": search,
          "results": JSON.stringify(res["data"])}
      }, '/results')
    }
  }

  return (
    <>
      <Head>
        <title>Search Engine</title>
        <link rel="icon" href="/favicon.png" />
      </Head>
      <main className='main'>
        <div className='header'>
          <span className="input-text">search: </span>
          <input type="text" className="textbox" ref={inputRef} onChange={handleChange} placeholder="start typing here" onKeyDown={onKeyDown} />
        </div>
      </main>
    </>
  )
}
