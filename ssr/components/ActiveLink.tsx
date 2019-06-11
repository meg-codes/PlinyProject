import * as React from 'react';
import { withRouter, WithRouterProps } from "next/router";
import Link from 'next/link';
import { LinkProps } from 'next/link';

interface Props extends WithRouterProps, LinkProps, {}

const ActiveLink:React.FC<Props> = ({ children, router, href, ...props}) => (
  <Link href={href} {...props}>
    {React.cloneElement(React.Children.only(children), {
      className: router.asPath === href ? `active` : null
    })}
  </Link>
)

export default withRouter(ActiveLink)
