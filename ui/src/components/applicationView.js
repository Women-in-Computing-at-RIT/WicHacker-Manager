import { Grommet, Box } from "grommet";
import NavBar from "./navBar";

export function ApplicationView({userData}) {
    console.log(userData)
    return(
        <Grommet>
            <Box>
                <NavBar title="Hacker Application" />
            </Box>
        </Grommet>
    //   <div className={css.applicationView}>
    //       <h2>Application Review</h2>
    //       <div className={css.dataPointWrapper}>
    //           <p className={css.dataLabel}>Name</p>
    //           <p className={css.data}>{userData.first_name} {userData.last_name}</p>
    //       </div>
    //       <div className={css.dataPointWrapper}>
    //           <p className={css.dataLabel}>Gender</p>
    //           <p className={css.data}>{userData.gender}</p>
    //       </div>
    //       <div className={css.dataPointWrapper}>
    //           <p className={css.dataLabel}>Major</p>
    //           <p className={css.data}>{userData.major}</p>
    //       </div>
    //       <div className={css.dataPointWrapper}>
    //           <p className={css.dataLabel}>Level Of Study</p>
    //           <p className={css.data}>{userData.level_of_study}</p>
    //       </div>
    //       <div className={css.dataPointWrapper}>
    //           <p className={css.dataLabel}>Birthday</p>
    //           <p className={css.data}>{userData.birthday}</p>
    //       </div>
    //       <div className={css.dataPointWrapper}>
    //           <p className={css.dataLabel}>Shirt Size</p>
    //           <p className={css.data}>{userData.shirt_size}</p>
    //       </div>
    //       <div className={css.dataPointWrapper}>
    //           <p className={css.dataLabel}>Has Previously Attended Hackathons</p>
    //           <p className={css.data}>{userData.has_attended_hackathons === 1 ? "True" : "False"}</p>
    //       </div>
    //       <div className={css.dataPointWrapper}>
    //           <p className={css.dataLabel}>Has Previously Attended WiCHacks</p>
    //           <p className={css.data}>{userData.has_attended_wichacks === 1 ? "True" : "False"}</p>
    //       </div>
    //       <div className={css.dataPointWrapper}>
    //           <p className={css.dataLabel}>Attending Online Only</p>
    //           <p className={css.data}>{userData.is_virtual ? "Yes" : "No"}</p>
    //       </div>
    //       <div className={css.dataPointWrapper}>
    //           <p className={css.dataLabel}>Dietary Restrictions</p>
    //           <p className={css.data}>{userData.dietary_restrictions ? userData.dietary_restrictions : "None"}</p>
    //       </div>
    //       <div className={css.dataPointWrapper}>
    //           <p className={css.dataLabel}>Dietary Restrictions</p>
    //           <p className={css.data}>{userData.special_accommodations ? userData.special_accommodations : "None"}</p>
    //       </div>
    //   </div>
    );
}