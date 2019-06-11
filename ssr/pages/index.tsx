import React from 'react';
import fetch from 'isomorphic-unfetch';
import moment from 'moment';

import ActiveLink from '../components/ActiveLink';

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
      <main>
      <h1>The Pliny Project</h1>
      <ActiveLink href='/'><a>Home</a></ActiveLink>
      <p>This site and its associated web application is a digital resource 
      for the correspondents of Pliny the Younger and his world,
      especially in its social dimensions and the connections between 
      his associates.</p>

      <p>Use the quick search or menu above to explore the site.</p>
      <Posts posts={this.props.posts} />
      </main>
    )
  }

  static async getInitialProps() {
    try {
      const res = await fetch('http://localhost:8000/api/posts');
      const data = await res.json();
      return {
        posts: data
      }
    } catch(exception) {
      console.log(exception)
    }
  }
}

