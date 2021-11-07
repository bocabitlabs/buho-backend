import { Col, Row } from "antd";
import SectorAddEditForm from "components/SectorAddEditForm/SectorAddEditForm";
import { MarketsContext } from "contexts/markets";
import WrapperPage from "pages/WrapperPage/WrapperPage";
import React, { useContext } from "react";
import SectorsAddPageHeader from "./components/SectorsAddHeader/SectorsAddHeader";

// Params are placeholders in the URL that begin
// with a colon, like the `:id` param defined in
// the route in this example. A similar convention
// is used for matching dynami§wc segments in other
// popular web frameworks like Rails and Express.

export default function SectorsAddPage() {
  const marketsContext = useContext(MarketsContext);

  return (
    <WrapperPage>
      <MarketsContext.Provider value={marketsContext}>
        <SectorsAddPageHeader>
          <Row>
            <Col>
              <SectorAddEditForm />
            </Col>
            <Col />
          </Row>
        </SectorsAddPageHeader>
      </MarketsContext.Provider>
    </WrapperPage>
  );
}
