import { memo } from 'react';
import { selectAuthUser } from '../../api/endpoints/auth.endpoint';
import { useCmtsQuery } from '../../api/endpoints/comment.endpoint';
import AddComment from './AddComment';
import Comment from './Comment';
import SS from '../util/SpinningCircle';
import { useAppSelector } from '../../store/hooks';
interface Props {
  projectId: number;
  issueId: number;
}

function CommentSection(props: Props) {
  const { projectId } = props;
  const authUser = useAppSelector(selectAuthUser);
  const { data: cmts } = useCmtsQuery(props, { refetchOnMountOrArgChange: true });

  if (!authUser) return null;

  return (
    <div className='mt-4 max-w-[35rem] py-3 text-c-text sm:mx-3'>
      <span className='font-medium tracking-wide'>Comments</span>
      <AddComment {...{ u: authUser, ...props }} />
      <ul className='mt-6'>
        {cmts ? (
          cmts.length > 0 ? (
            cmts.map((cmt) => <Comment key={cmt.id} {...{ ...cmt, u: authUser, projectId }} />)
          ) : (
            <span className='ml-11 text-gray-700'># no comments yet</span>
          )
        ) : (
          <span>loading comments...</span>
        )}
      </ul>
    </div>
  );
}

export default memo(CommentSection);
