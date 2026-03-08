import React, { useEffect, useState } from 'react';
import axios from 'axios';

const Dashboard: React.FC = () => {
    const [platforms, setPlatforms] = useState([]);
    const [targets, setTargets] = useState([]);

    useEffect(() => {
        const fetchData = async () => {
            const token = localStorage.getItem('token');
            const config = { headers: { Authorization: `Bearer ${token}` } };
            try {
                const pRes = await axios.get('/config/platforms', config);
                const tRes = await axios.get('/config/targets', config);
                setPlatforms(pRes.data);
                setTargets(tRes.data);
            } catch (error) {
                console.error('Failed to fetch config', error);
            }
        };
        fetchData();
    }, []);

    return (
        <div>
            <h2>Dashboard</h2>
            <h3>Platforms</h3>
            <ul>{platforms.map((p: any) => <li key={p.id}>{p.name}</li>)}</ul>
            <h3>Targets</h3>
            <ul>{targets.map((t: any) => <li key={t.id}>{t.name} ({t.target_url})</li>)}</ul>
        </div>
    );
};

export default Dashboard;
