import { Routes, Route } from "react-router-dom";
import PageNotFound from "../pages/404Page";
import WiCHacksLanding from "../pages/wichacksLanding";
import { ProtectedComponent } from "../hocs/protectedRoute";
import UserHomepage from "../pages/hackers/hackerLanding";
import {NewAdminForm, NewHackerForm} from "../pages/hackers/createNewUser";
import HackerApplication from "../pages/hackers/application";
import HackerApplicationView from "../pages/hackers/hackerApplicationView";
import LoadingView from "../pages/LoadingView";
import {AdminRoute} from "../hocs/adminRoute";
import HackathonManagerLandingPage from "../pages/manage/hmLanding";
import ManageApplications from "../pages/manage/manageApplications";
import {CONSOLE, HACKER_DATA, READ} from "../utils/constants";

export default function AppRoutes(){
    return (
        <Routes>
            <Route path="/" element={<WiCHacksLanding />}/>
            <Route path="/user" element={<ProtectedComponent component={UserHomepage} />} />
            <Route path="/user/create" element={<ProtectedComponent component={NewHackerForm} />} />
            <Route path="/user/apply" element={<ProtectedComponent component={HackerApplication} />} />
            <Route path="/user/application" element={<ProtectedComponent component={HackerApplicationView} />} />
            <Route path="/auth" element={<LoadingView />} />
            <Route path="/manage" element={<ProtectedComponent component={AdminRoute} permission={CONSOLE} type={READ} children={<HackathonManagerLandingPage />} />} />
            <Route path="/manage/applications" element={<ProtectedComponent component={AdminRoute} permission={HACKER_DATA} type={READ} children={<ManageApplications />} />} />
            <Route path="/manage/admin/signup" element={<ProtectedComponent component={AdminRoute} permission={CONSOLE} type={READ} children={<NewAdminForm />} />} />
            <Route path="/notFound" element={<PageNotFound />} />
            <Route path="*" element={<PageNotFound />} />
        </Routes>
    )
}