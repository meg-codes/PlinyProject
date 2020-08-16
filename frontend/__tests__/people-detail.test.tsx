/* eslint-env jest */
import { shallow } from "enzyme";
import PersonDetail from "../pages/people-detail";
import MockAdapter from "axios-mock-adapter";
import axios from "axios";
import { tacitus, fakeDatesTacitus } from "./__fixtures__/people-fixtures";
import ExpressContext from "../lib/app-context";

process.env.NEXT_BASE_URL = "";

describe("Person Detail", () => {
  let mock: MockAdapter;

  beforeEach(() => {
    mock = new MockAdapter(axios);
  });

  it("should render a message if an empty object is passed as a prop", () => {
    const persondetail = shallow(
      <PersonDetail id={1} person={undefined}></PersonDetail>
    );
    expect(persondetail.find("h1").text()).toEqual("No person data loaded.");
  });

  it("should render api data passed as a prop", () => {
    const persondetail = shallow(
      <PersonDetail id={1} person={tacitus}></PersonDetail>
    );
    expect(persondetail.find("h1").text()).toBe(tacitus.nomina);
    expect(persondetail.find(".person-details").html()).toMatchSnapshot();
  });

  it("should handle all dates that may be passed to it", () => {
    const persondetail = shallow(
      <PersonDetail id={1} person={fakeDatesTacitus}></PersonDetail>
    );
    expect(persondetail.find(".person-details").html()).toMatchSnapshot();
  });

  it("should use getInitialProps to make an api call with a correct url.", () => {
    const query = {
      id: 1,
    };
    mock.onGet("/api/people/1").reply(200, tacitus);
    expect.assertions(2);
    const context = ({
      query: query,
      res: undefined,
      req: undefined,
    } as unknown) as ExpressContext;
    return PersonDetail.getInitialProps(context).then((props) => {
      expect(props.id).toBe(1);
      expect(props.person).toEqual(tacitus);
    });
  });

  it("should handle a call on the server side", () => {
    mock.onGet("/api/people/1").reply(200, tacitus);

    const context = ({
      query: { id: 1 },
      req: {
        protocol: "http",
        get: (key: string) => {
          if (key === "Host") return "localhost:3000";
        },
        url: "cornelius-tacitus-1",
      },
      res: {
        writeHead: jest.fn(),
        end: jest.fn(),
      },
    } as unknown) as ExpressContext;
    mock.onGet("http://localhost:3000/api/people/1").reply(200, tacitus);
    if (context.res) {
      expect.assertions(4);
    } else {
      expect.assertions(2);
    }
    return PersonDetail.getInitialProps(context).then((props) => {
      expect(props.id).toBe(1);
      expect(props.person).toEqual(tacitus);
      if (context.res) {
        expect(context.res.writeHead).toBeCalledTimes(0);
        expect(context.res.end).toBeCalledTimes(0);
      }
    });
  });

  it("should rewrite the url if a request for wrong full url comes in", () => {
    mock.onGet("/api/people/1").reply(200, tacitus);
    const context = ({
      query: { id: 1 },
      req: {
        protocol: "http",
        get: (key: string) => {
          if (key === "Host") return "localhost:3000";
        },
        url: "foobar-test-1",
      },
      res: {
        writeHead: jest.fn(),
        end: jest.fn(),
      },
    } as unknown) as ExpressContext;
    expect.assertions(2);
    return PersonDetail.getInitialProps(context).then(() => {
      if (context.res) {
        expect(context.res.writeHead).toBeCalledWith(302, {
          Location: "/people/cornelius-tacitus-1",
        });
        expect(context.res.end).toBeCalled();
      }
    });
  });

  it("should return an undefined person on network error on initial props", () => {
    mock.onGet("/api/people/1").reply(500);
    const context = ({
      query: { id: 1 },
    } as unknown) as ExpressContext;
    expect.assertions(2);
    return PersonDetail.getInitialProps(context).then((props) => {
      expect(props.id).toBe(1);
      expect(props.person).toBeUndefined();
    });
  });
});
