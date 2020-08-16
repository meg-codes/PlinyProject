import * as React from "react";
import { withRouter } from "next/router";
import Link from "next/link";
import { LinkProps } from "next/link";
import { WithRouterProps } from "next/dist/client/with-router";

interface ActiveLinkProps extends WithRouterProps, LinkProps {}

export const ActiveLink: React.FC<ActiveLinkProps> = ({
  children,
  router,
  href,
  ...props
}) => (
  <Link href={href} {...props}>
    {React.cloneElement(React.Children.only(children as any), {
      className: href === router.pathname ? `active` : null,
    })}
  </Link>
);

export default withRouter(ActiveLink);
