import React from 'react';
import Link from 'next/link';
import { Button,
         Row,
         Col } from 'reactstrap';


const PageButtons = ({ href, as, next_page, prev_page }) => {

  return (
    <Row className="mt-4 mb-5">

        { prev_page !== null &&
          <Link href={{ pathname: href, query: { page: prev_page } }}
                as={`${as}?page=${prev_page}`}>
            <a>
              <Button outline className="mx-2">
              <i className="fas fa-arrow-left" /> previous
              </Button>
            </a>
          </Link>
        }

        { next_page &&
            <Link href={{ pathname: href, query: { page: next_page } }}
                  as={`${as}?page=${next_page}`}>
              <a>
                <Button outline className="mx-2">
                  next <i className="fas fa-arrow-right" />
                </Button>
              </a>
            </Link>
          }
    </Row>
  )
}

export default PageButtons;