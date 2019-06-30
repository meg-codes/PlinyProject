import * as React from 'react';
import axios from 'axios';
import moment from 'moment';
import Head from 'next/head';

import Header from '../components/Header';

interface Post {
  id: number,
  date_updated: Date,
  subject: string,
  content: string
}

type HomeProps = {
  posts: Post[]
}

const Posts: React.FC<{ posts: Post[] }> = ({ posts }) =>
  <section>
    <h2>News</h2>
    <hr/>
    <div id='articles'>
    {posts.map(post => (
      <article key={post.id}>
        <h3>{ post.subject }</h3>
        <p>{ post.content }</p>
        <small>{ moment(post.date_updated).format('D MMM YYYY') }</small>
      </article>
    ))}
    </div>
  </section>

export default class Home extends React.Component<HomeProps> {
  
  constructor(props: HomeProps) {
    super(props);
  }

  render() {
    return (
      <React.Fragment>
      <Head>
        <title>The Pliny Project</title>
      </Head>
      <Header />
      <main>
        <h1>The Pliny Project</h1>
      <p>This site and its associated web application are a digital resource 
      for the correspondents of Pliny the Younger and his world,
      especially in its social dimensions and the connections between 
      his associates.</p>

      <p>Use the quick search or menu above to explore the site.</p>
      <Posts posts={this.props.posts} />
      </main>
      </React.Fragment>
    )
  }

  static async getInitialProps({ req }: any) {
    try {
      const baseUrl = req ? `${req.protocol}://${req.get('Host')}` : '';
      const res = await axios.get(baseUrl + '/api/posts');
      return {
          posts: res.data
      }
    } catch(err) {
      return {
        posts: []
      }
    }
  }

}
