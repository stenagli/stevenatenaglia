import { type CollectionEntry, getCollection } from 'astro:content';

export async function getStaticPaths() {
  const posts = await getCollection('content');
  return posts.map((post) => ({
    params: { slug: post.id },
    props: post,
  }));
}

export type Props = CollectionEntry<'content'>;
